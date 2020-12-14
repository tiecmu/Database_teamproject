<?php
    $link = mysqli_connect("localhost","wotjd2979","123456", "k_covid19");
    if( $link === false )
    {
        die("ERROR: Could not connect. " . mysqli_connect_error());
    }
    echo "Coneect Successfully. Host info: " . mysqli_get_host_info($link) . "\n";
?>
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
    <h1 style="text-align:center"> Patient Information by Infection case </h1>
    <hr style = "border : 5px solid yellowgreen">
    
    <p> 
       <h3>Select Infection case</h3>
    </p>
    <?php
	$action = '';
	if(isset($_POST['action']))$action = $_POST['action'];
        
        $current_select = '-';
	if($action == 'form_submit') {
            $current_select = $_POST['infection_case'];
            echo '<xmp>';
            
            if($current_select == '-'){}
            else if($current_select == '') {
                echo 'Searching patient information by NULL';
            }
            else {
                echo 'Searching patient information by '.$current_select;
            }
            echo '</xmp>';
	}
    ?>
    <form method="post" action="<?=$_SERVER['PHP_SELF']?>">
	<input type="hidden" name="action" value="form_submit" />
        <select name="infection_case">
            echo '<option value='-'>----------------------- Select ---------------------------</option>'
  	<?php
            $sql = "select * from patientinfo";
            $result = mysqli_query($link,$sql);
            
            $infection_case_array = array();
            while( $row_list = mysqli_fetch_assoc($result)  )
            {
                array_push($infection_case_array, $row_list['infection_case']);
            }
            
            $infection_case_unique_array = array_unique($infection_case_array);
            
            foreach ($infection_case_unique_array as $infection_case){
                if($infection_case != '') {
                    echo '<option value="', $infection_case, '">', $infection_case, '</option>';
                } else {
                    echo '<option value="', $infection_case, '">NULL</option>';
                }
            }
        ?>
        </select>
  	<input type="submit" value="Load" />
    </form>
    <?php
        if($current_select == '-') {
            $sql = "select count(*) as num from patientinfo";
        } elseif($current_select == '') {
            $sql = "select count(*) as num from patientinfo where infection_case is null;";
        } else {
            $sql = "select count(*) as num from patientinfo where infection_case=\"".$current_select."\"";
        }
        $result = mysqli_query($link, $sql);
        $data = mysqli_fetch_assoc($result);
    ?>
    <p>
        <h3>Patient Info table (Currently <?php echo $data['num']; ?>)  patients <?php if($current_select != '-') {echo "by ".$current_select;} ?> in database </h3>
    </p>

    <table cellspacing="0" width="100%">
        <thead>
        <tr>
            <th>Patient_ID</th>
            <th>Sex</th>
            <th>Age</th>
            <th>Country</th>
            <th>province</th>
            <th>City</th>
            <th>Infection_Case</th>
            <th>Infected_by</th>
            <th>contact_number</th>
            <th>symptom_onset_date</th>
            <th>confirmed_date</th>
            <th>released_date</th>
            <th>deceased_date</th>
            <th>state</th>
            <th>hospital_id</th>
        </tr>
        </thead>
        <tbody>
         
            <?php
                if($current_select == '-') {
                    $sql = "select * from patientinfo";
                } elseif($current_select == '') {
                    $sql = "select * from patientinfo where infection_case is null";
                } else {
                    $sql = "select * from patientinfo where infection_case=\"".$current_select."\"";
                }
                $result = mysqli_query($link,$sql);
                while( $row = mysqli_fetch_assoc($result))
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