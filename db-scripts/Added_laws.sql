do $$
declare 
    i            integer      := 0;
    v_law_number varchar(20)  := '149-ФЗ';
    v_law_title  varchar(200) := 'Об информации, информационных технологиях и о защите информации';
	v_law_date   date         := to_date('27.07.2006', 'dd.mm.yyyy');
begin
    raise notice '----';
    --
	select count(*)
	  into i
	  from public.rest_laws r
      where r.law_number = v_law_number ;
	--
    if i != 0 then
	    raise notice 'Закон % ранее был добавлен', v_law_number;
    else
  		raise notice 'Закон % ранее не был добавлен', v_law_number;
		--
		INSERT INTO public.rest_laws
		(law_number, law_title, law_date)
		VALUES(v_law_number, v_law_title, v_law_date);
 	end if;
	--
    commit;
end $$;