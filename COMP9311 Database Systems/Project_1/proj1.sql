
-- COMP9311 18s1 Project 1
--
-- MyMyUNSW Solution Template


-- Q1: 
create or replace view Q1(unswid, name)
as
--... SQL statements, possibly using other views/functions defined by you ...
select distinct p.unswid, p.name 
from people p 
	join students s on p.id = s.id
where s.stype = 'intl'
	and s.id in    (select p.id 
					from people p
					 	join course_enrolments c on p.id = c.student
					where c.mark >= 85
					group by p.id
					having count(c) > 20
				   )
;



-- Q2: 
create or replace view Q2(unswid, name)
as
--... SQL statements, possibly using other views/functions defined by you ...
select distinct r.unswid, r.longname as name
from rooms r 
	join room_types t on r.rtype = t.id
	join buildings b on b.id = r.building
where t.description = 'Meeting Room'
	and r.capacity >= 20
	and b.name = 'Computer Science Building'
;



-- Q3: 
create or replace view Q3(unswid, name)
as
--... SQL statements, possibly using other views/functions defined by you ...
select distinct p.unswid, p.name 
from people p
	join staff s on p.id = s.id
	join course_staff c on c.staff = s.id
where c.course in  (select c.course from course_enrolments c
				    	join students s on s.id = c.student
						join people p on p.id = s.id
				    where p.name = 'Stefan Bilek'
				   )
;



-- Q4:
create or replace view Q4(unswid, name)
as
--... SQL statements, possibly using other views/functions defined by you ...
select distinct p.unswid, p.name
from people p
	join students s on p.id = s.id
	join course_enrolments ce on ce.student = s.id
	join courses c on c.id = ce.course
	join subjects sb on sb.id = c.subject
where sb.code = 'COMP3331'
	and s.id not in    (select s.id from students s
							join course_enrolments ce on ce.student=s.id
							join courses c on c.id=ce.course
							join subjects sb on sb.id= c.subject
					 	where sb.code='COMP3231'
					   )
;



-- Q5: 
create or replace view Q5a(num)
as
--... SQL statements, possibly using other views/functions defined by you ...
select count(distinct s.id) as num
from students s
	join program_enrolments pe on s.id = pe.student
	join stream_enrolments se on se.partof = pe.id
	join streams st on st.id = se.stream
	join semesters ss on ss.id = pe.semester
where s.stype = 'local'
	and st.name = 'Chemistry'
	and ss.term = 'S1'
	and ss.year = 2011
;

-- Q5: 
create or replace view Q5b(num)
as
--... SQL statements, possibly using other views/functions defined by you ...
select count(distinct s.id) as num
from students s 
	join program_enrolments pe on s.id = pe.student
	join semesters ss on ss.id = pe.semester
	join programs pr on pr.id = pe.program 
	join orgunits org on org.id = pr.offeredby
where s.stype = 'intl'
	and ss.term = 'S1'
	and ss.year = 2011
	and org.longname = 'School of Computer Science and Engineering'
;


-- Q6:
create or replace function Q6(text) returns text
as
$$
--... SQL statements, possibly using other views/functions defined by you ...
select s.code||' '||s.name||' '||s.uoc
from subjects s 
where s.code = $1
$$ language sql;



-- Q7: 
create or replace view Q7(code, name)
as
--... SQL statements, possibly using other views/functions defined by you ...
select p.code, p.name
from students s 
	join program_enrolments pe on pe.student = s.id
	join programs p on p.id = pe.program
where p.id in  (select p.id
			    from students s 
			        join program_enrolments pe on pe.student = s.id
			        join programs p on p.id = pe.program
		        group by p.id
		        having count(case when s.stype = 'intl' then p.id end)::numeric/count(s.id)::numeric > 0.5
			   )
group by p.id
;



-- Q8:
create or replace view Q8(code, name, semester)
as
--... SQL statements, possibly using other views/functions defined by you ...
select sb.code, sb.name, sm.name as semester
from courses c 
	join subjects sb on c.subject = sb.id
	join semesters sm on sm.id = c.semester
where c.id in
   (select distinct c.id 
		from courses c
			join course_enrolments ce on ce.course = c.id
		group by c.id
		having avg(ce.mark) = 
-- max		
		   (select max(avg)
-- avg			
			from   (select avg(ce.mark) as avg
					from courses c
						join course_enrolments ce on ce.course = c.id
-- not null >= 15					
					where c.id in 
					   (select c.id
						from courses c
							join course_enrolments ce on ce.course = c.id
						where ce.mark is not null
						group by c.id
						having count(ce.mark) >= 15
					   )
					group by c.id
				   )as avg_table
		   )
   )
;



-- Q9:
create or replace view Q9(name, school, email, starting, num_subjects)
as
--... SQL statements, possibly using other views/functions defined by you ...
select p.name, o.longname, p.email, a.starting, num.num_sub
from   (select p.id as id, count(distinct sb.code) as num_sub
    	from people p
			join staff s on p.id = s.id
			join affiliations a on a.staff = s.id
			join staff_roles sr on sr.id = a.role
			join orgunits o on o.id = a.orgunit 
			join orgunit_types ot on ot.id = o.utype
			join course_staff cs on cs.staff = s.id
			join courses c on cs.course = c.id
			join subjects sb on sb.id = c.subject
		where sr.name = 'Head of School'
			and a.ending is null
			and a.isprimary = true
			and ot.name = 'School'
		group by p.id
	   ) as num
	join people p on p.id = num.id
	join staff s on p.id = s.id
	join affiliations a on a.staff = s.id
	join orgunits o on o.id = a.orgunit
	join staff_roles sr on sr.id = a.role
	join orgunit_types ot on ot.id = o.utype
where sr.name = 'Head of School'
	and a.ending is null
	and a.isprimary = true
	and ot.name = 'School'
;



-- Q10:
create or replace view Q10(code, name, year, s1_HD_rate, s2_HD_rate)
as
--... SQL statements, possibly using other views/functions defined by you ...
select s.code,s.name,substring(to_char(ss.year,'9999'), 4, 2) as year,
	s1.rate as s1_HD_rate,s21.rate as s2_HD_rate
from subjects s 
	join courses c on c.subject=s.id
	join semesters ss on ss.id=c.semester
	join(
		select (count(case when ce.mark>=85 then c.id end)::numeric
				/count(case when ce.mark>=0 then c.id end)::numeric)::numeric(4,2) 
				as rate,c.id as id
		from course_enrolments ce
			join courses c on c.id=ce.course
			join subjects s on s.id=c.subject
			join semesters ss on ss.id=c.semester
		where s.id in 
			(
			select s.id
			from subjects s 
				join courses c on c.subject=s.id
				join semesters ss on ss.id=c.semester
			where ss.term='S1'
				and s.code like'%COMP93%'
				and ss.year between 2003 and 2012
			group by s.id
			having count(ss.year)=10
			intersect
			select s.id
			from subjects s 
				join courses c on c.subject=s.id
				join semesters ss on ss.id=c.semester
			where ss.term='S2'
				and s.code like'%COMP93%'
				and ss.year between 2003 and 2012
			group by s.id
			having count(ss.year)=10
			)
			and ss.year between 2003 and 2012
			and ss.term='S1'
		group by c.id
		) as s1 on s1.id=c.id

	join(
		select s.code as code,ss.year as year, s2.rate as rate
		from subjects s 
			join courses c on c.subject=s.id
			join semesters ss on ss.id=c.semester
			join(
				select (count(case when ce.mark>=85 then c.id end)::numeric
					/count(case when ce.mark>=0 then c.id end)::numeric)::numeric(4,2) 
					as rate,c.id as id
				from course_enrolments ce
					join courses c on c.id=ce.course
					join subjects s on s.id=c.subject
					join semesters ss on ss.id=c.semester
				where s.id in 
					(
					select s.id
					from subjects s 
						join courses c on c.subject=s.id
						join semesters ss on ss.id=c.semester
					where ss.term='S1'
						and s.code like'%COMP93%'
						and ss.year between 2003 and 2012
					group by s.id
					having count(ss.year)=10
					intersect
					select s.id
					from subjects s 
						join courses c on c.subject=s.id
						join semesters ss on ss.id=c.semester
					where ss.term='S2'
						and s.code like'%COMP93%'
						and ss.year between 2003 and 2012
					group by s.id
					having count(ss.year)=10
					)
					and ss.year between 2003 and 2012
					and ss.term='S2'
					group by c.id
				) as s2 on s2.id=c.id
		) as s21 on s21.year=ss.year and s21.code=s.code
	order by s.code, ss.year
;
















