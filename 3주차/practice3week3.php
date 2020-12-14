//3주차 3번 테이블 만들기문제입니다
<?php
    $link = mysqli_connect("localhost","wotjd2979","123456", "k_covid19");
    if( $link === false )
    {
        die("ERROR: Could not connect. " . mysqli_connect_error());
    }
    echo "Coneect Successfully. Host info: " . mysqli_get_host_info($link) . "\n";
?>//php랑 html 연결했음
<style>
    table {
        width: 100%;
        border: 1px solid #444444;
        border-collapse: collapse;
    }
    th, td {
        border: 1px solid #444444;
    }
</style>
<body>
    <h1 style="text-align:center"> 데이터베이스 팀 프로젝트 3주차 3번 테이블 만들기 </h1>
    <hr style = "border : 5px solid yellowgreen">
    <?php

        $sql = "drop view table1";
        mysqli_query($link,$sql);
        $sql = "drop view result";
        mysqli_query($link,$sql);
        $sql = "drop table tempo";
        mysqli_query($link,$sql);

        $query = "create view table1 as
        select c.infection_case as c1 ,c.province as cz, c.city as c2, r.academy_ratio as c3, r.elderly_population_ratio as c4, c.confirmed as c5
        from caseinfo c, region r, patientinfo p
        where c.province = r.province and c.infection_group = 1 and p.infection_case=c.infection_case
        group by c.infection_case
        order by confirmed desc";
        mysqli_query($link,$query);

        $query = "create table tempo(
            infection_case char(70), 
            age char(10), 
            primary key(infection_case))";
        mysqli_query($link,$query);


        $sql = "select distinct c.infection_case
        from patientinfo p, caseinfo c 
        where p.infection_case is not null and c.infection_group=1";
        $result=mysqli_query($link,$sql);
        // echo "<xmp>";
        // echo $result;
        // echo "</xmp>";

        while($row =mysqli_fetch_array($result)){
            $variable=$row['infection_case'];
            $query="insert into tempo (infection_case,age) 
            select t.ic,t.a1 from
            (select p.infection_case as ic, p.age as a1
            from patientinfo p
            where p.infection_case=\"".$variable."\" 
            group by p.age
            order by count(p.age) desc limit 1
            )as t ;";
            mysqli_query($link,$query);
        }
        $query="create view result as
        select t1.c1, t1.cz,t1.c2,t1.c3, t1.c4, t1.c5, tempo.age 
        from table1 t1
        join tempo
        on t1.c1=tempo.infection_case";
        mysqli_query($link,$query);

    ?>
    

    <table cellspacing="0" width="100%">
        <thead>
        <tr>
            <th>Infection_case</th>
            <th>Province</th>
            <th>city</th>
            <th>academy_ratio</th>
            <th>elderly_population_ratio</th>
            <th>confirmed</th>
            <th>the greater part of</th>
        </tr>
        </thead>
        <tbody>
            <?php
                $query="select * from result";
                $result=mysqli_query($link,$query);
                // echo "<xmp>";
                // echo $result;
                // echo "</xmp>";
                while( $row = mysqli_fetch_row($result)  )
                {
                    print "<tr>";
                    foreach($row as $key => $val)
                    {
                        print "<td>" . $val . "</td>";
                    }
                    print "</tr>";
                }
            ?>
            
        </tbody>
    </table>
</body>



