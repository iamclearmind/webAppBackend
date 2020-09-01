

CREATE TABLE if not exists public.benchmark_master
(
    id serial PRIMARY KEY,
    exchange character varying(20) NOT NULL,
    benchmark character varying(20) NOT NULL,
    market_type character varying(20) NOT NULL,
    sector character varying(50),
    UNIQUE (exchange, benchmark, sector)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

--ALTER TABLE public.benchmark_master
--    OWNER to postgres;


CREATE TABLE if not exists public.datasource_master
(
    id serial PRIMARY KEY,
	exchange character varying(20) NOT NULL,
    timeframe_m INTEGER NOT NULL,
    resample_tf integer[],
    market_type character varying(20) NOT NULL,
    path character varying(500),
	handler_path character varying(200),
	isactive character varying(5) NOT NULL,
	created_timestamp timestamp default now(),
	last_updated timestamp default now(),
	unique(exchange,timeframe_m),
	unique(path)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

--ALTER TABLE public.datasource_master
  --  OWNER to streamer;
	

CREATE TABLE  if not exists public.scrip_master
(
    id serial PRIMARY KEY,
	scrip_code character varying(20) NOT NULL,
    company_name character varying(50) NOT NULL,
	market_type character varying(20) NOT NULL,
    exchange character varying(200),
    timeframe INTEGER NOT NULL,
    file_name varchar(200) NOT NULL,
	isactive character varying(5) NOT NULL,
	created_timestamp timestamp default now(),
	last_updated timestamp default now(),
	unique(scrip_code,file_name)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

--ALTER TABLE public.scrip_master
  --  OWNER to streamer;	
	
CREATE TABLE  if not exists public.composite_scrip_master
(
    id serial PRIMARY KEY,
	scrip_code_x_y character varying(20) NOT NULL,
    scrip_code_x character varying(20) NOT NULL,
	scrip_code_y character varying(20) NOT NULL,
    operator character varying(40),
	created_timestamp timestamp default now(),
	last_updated timestamp default now()
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

--ALTER TABLE public.composite_scrip_master
  --  OWNER to streamer;	

CREATE TABLE  if not exists public.composite_scrip_ohlc
(
    id serial PRIMARY KEY,
	scrip_code character varying(20) NOT NULL,
    "timestamp"  timestamp,
	close real,
	created_timestamp timestamp default now(),
	last_updated timestamp default now()
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

--ALTER TABLE public.composite_scrip_ohlc
  --  OWNER to streamer;
	
CREATE TABLE IF NOT EXISTS public.data_error_log
(
    id  serial PRIMARY KEY,
	scrip_code_id_list integer[] NOT NULL,
    error text  NOT NULL,
    exchange character varying(30)  NOT NULL,
	functin_name character varying(50),
	created_date timestamp without time zone default now()
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

--ALTER TABLE public.data_error_log
  --  OWNER to streamer;
    
CREATE TABLE if not exists public.screener_master
(
    id  serial PRIMARY KEY,
    screener_name character varying(200) NOT NULL,
    data_table_id character varying(100) NOT NULL,
    sector character varying(50) ,
    screener_file character varying(200) NOT NULL,
    output_colomns character varying(2000) ,
    csv_output_path character varying(2000) NOT NULL,
    isdeleted character varying(5)  NOT NULL,
    unique(data_table_id,sector),
    unique(screener_name)
)
WITH (
    OIDS = FALSE
)

TABLESPACE pg_default;

--ALTER TABLE public.screener_master
--    OWNER to postgres;

CREATE TABLE if not exists public.screener_value_table
(
    id  serial PRIMARY KEY,
    screener_name character varying(200) NULL,
    date_time timestamp without time zone NOT NULL,
    data_json json NOT NULL,
    last_updated timestamp without time zone NOT NULL,
    unique(screener_name, date_time)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

--ALTER TABLE public.screener_value_table
--    OWNER to postgres;
    
Create or replace function disable_scrip_code(in_days integer,in_timeframe integer,
												in_exchange character varying(20),
												in_market_type character varying(50),
												in_table_name character varying(100)
											 )
RETURNS integer
AS
$$
	 BEGIN
	 
			EXECUTE format('update scrip_master as sm
			set isactive = (case when ((t2.t_days > 0 and t2.t_days < %s)) then ''t'' 
								when t2.t_days = 0 then ''y'' 
								else ''n'' 
								end
							)
			from 
			(select scrip_code,DATE_PART(''day'',now()::timestamp - last_datetime::timestamp) as t_days 
			from (select scrip_code,max(datetime)  last_datetime from %s
								group by scrip_code order by last_datetime desc) as t1
			where DATE_PART(''day'',now()::timestamp - last_datetime::timestamp) >= 0) as t2
			where t2.scrip_code = sm.scrip_code and sm.timeframe = %s and sm.exchange = ''%s'' and sm.market_type = ''%s''', in_days,in_table_name,in_timeframe,in_exchange,in_market_type);
			
			
			EXECUTE format('insert into data_error_log(scrip_code_id_list,error,exchange,functin_name)
							select ARRAY_AGG(sm.id),t2.status,''%s'',''ohlcv_csv_to_db'' from scrip_master sm
							inner join 
							(select scrip_code,case when DATE_PART(''day'',now()::timestamp - last_datetime::timestamp) > 0 and 
														DATE_PART(''day'',now()::timestamp - last_datetime::timestamp) < %s then ''temporary_inactive''
														else ''permanent_inactive'' end as status
										from (select scrip_code,max(datetime)  last_datetime from %s
															group by scrip_code order by last_datetime desc) as t1
										where DATE_PART(''day'',now()::timestamp - last_datetime::timestamp) > 0) as t2
							on t2.scrip_code = sm.scrip_code
							group by t2.status',in_exchange,in_days,in_table_name);
			
			RETURN 1;
					
	END; 
$$
LANGUAGE plpgsql;	

Create or replace function resample_daily_to_weekly(
												in_from_table character varying(100),
												in_to_table character varying(100)
											 )
RETURNS integer
AS
$$
		DECLARE
		day_of_week real :=  EXTRACT(DOW FROM  now());
		minus_dow real;
	 BEGIN			
					minus_dow := case when day_of_week in (0,6) then 0
									else day_of_week 
								 end;
					EXECUTE format('INSERT INTO %s
								(scrip_code,"datetime",open,high,low,close,volume)
					select scrip_code,
					datetime- (EXTRACT(DOW FROM  datetime) -1 || '' day'')::interval as dt,
					(array_agg(open ORDER BY datetime ASC))[1] o,
					MAX(high) h,
					MIN(low) l,
					(array_agg(close ORDER BY datetime DESC))[1] c,
					SUM(volume) vol
					from %s 
					where datetime <= now()-(%s || '' day'')::interval
					group by scrip_code,dt
					order by dt desc
					ON CONFLICT (scrip_code, datetime)
					DO UPDATE 
					SET
					open = excluded.open,
					high = excluded.high,
					low = excluded.low,
					close = excluded.close,
					volume = excluded.volume',in_to_table,in_from_table,minus_dow);
			
			RETURN 1;
					
	END; 
$$
LANGUAGE plpgsql;	

Create or replace function resample_daily_to_monthly(
												in_from_table character varying(100),
												in_to_table character varying(100)
											 )
RETURNS integer
AS
$$
	 BEGIN			
					EXECUTE format('INSERT INTO %s
								(scrip_code,"datetime",open,high,low,close,volume)
					select scrip_code,
					datetime- (EXTRACT(day FROM  datetime) -1 || '' day'')::interval as dt,
					(array_agg(open ORDER BY datetime ASC))[1] o,
					MAX(high) h,
					MIN(low) l,
					(array_agg(close ORDER BY datetime DESC))[1] c,
					SUM(volume) vol
					from %s
					group by scrip_code,dt
					order by dt desc
					ON CONFLICT (scrip_code, datetime)
					DO UPDATE 
					SET
					open = excluded.open,
					high = excluded.high,
					low = excluded.low,
					close = excluded.close,
					volume = excluded.volume',in_to_table,in_from_table);
			
			RETURN 1;
					
	END; 
$$
LANGUAGE plpgsql;

INSERT INTO public.benchmark_master(exchange, benchmark, market_type, sector)
VALUES ('ns', '.NSEI', 'equity','' ),
 ('bo', '.NSEI', 'equity', '')
 ON CONFLICT (exchange, benchmark, sector)
 DO UPDATE SET
market_type  = excluded.market_type;

INSERT INTO public.datasource_master(exchange, timeframe_m, resample_tf, market_type, path, handler_path, isactive)
VALUES ('ns', 1440, '{10080}', 'equity', '/opt/metastock/NSE/', 'metastock_handler', 'y'),
 ('index', 1440, '{10080}', 'equity', '/opt/metastock/ASIAN INDICES/', 'metastock_handler', 'y'),
 ('bo', 1440, '{10080}', 'equity', '/opt/metastock/BSE/', 'metastock_handler', 'y')
 ON CONFLICT (exchange,timeframe_m)
 DO UPDATE SET
resample_tf  = excluded.resample_tf,
market_type  = excluded.market_type,
path  = excluded.path,
handler_path = excluded.handler_path;
	
INSERT INTO public.screener_master(screener_name, data_table_id, sector, screener_file, output_colomns, csv_output_path, isdeleted)
VALUES ('cmOne_bo','ohlcv_bo_equity_10080', 'all','cmOne','', 'output_csv/','n'),
 ('cmOne_ns','ohlcv_ns_equity_10080', 'all','cmOne','', 'output_csv/','n'),
 ('Test_screen','ohlcv_ns_equity_10080', 'TAMO.NS','cmOne','', 'output_csv/','n')
  ON CONFLICT (data_table_id,sector)
 DO UPDATE SET
screener_name   = excluded.screener_name,
screener_file   = excluded.screener_file,
output_colomns   = excluded.output_colomns,
csv_output_path   = excluded.csv_output_path;
		
INSERT INTO public.scrip_master(scrip_code,company_name,market_type,exchange,timeframe,file_name, isactive)
VALUES ('LBES.BO','RELIANCE ETF LIQUID BEES', 'equity','bo','1440', 'LBES.BO#RELIANCE ETF LIQUID BEES (D).csv','n')
 ON CONFLICT (scrip_code,file_name)
DO UPDATE SET
market_type = excluded.market_type,
exchange = excluded.exchange,
company_name = excluded.company_name;

