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
    <h1 style="text-align:center"> Region Information By Province </h1>
    <hr style = "border : 5px solid yellowgreen">

    <p> 
       <h3>Select Province</h3>
    </p>

    <?php
	$action = '';
	if(isset($_POST['action']))$action = $_POST['action'];
        
        $current_select = '-';
	if($action == 'form_submit') {
            $current_select = $_POST['province'];
            echo '<xmp>';
            
            if($current_select == '-'){}
            else if($current_select == '') {
                echo 'Searching region information by NULL';
            }
            else {
                echo 'Searching region information by '.$current_select;
            }
            echo '</xmp>';
	}
    ?>
    <form method="post" action="<?=$_SERVER['PHP_SELF']?>">
	<input type="hidden" name="action" value="form_submit" />
        <select name="province">
            echo '<option value='-'>----------------------- Select ---------------------------</option>'
  	<?php
            $sql = "select * from region";
            $result = mysqli_query($link,$sql);
            
            $province_array = array();
            while( $row_list = mysqli_fetch_assoc($result)  )
            {
                array_push($province_array, $row_list['province']);
            }
            
            $province_unique_array = array_unique($province_array);
            
            foreach ($province_unique_array as $province){
                echo '<option value="', $province, '">', $province, '</option>';
            }
        ?>
        </select>
  	<input type="submit" value="Load" />
    </form>
    <?php
        if($current_select == '-') {
            $sql = "select count(*) as num from region";
        } else {
            $sql = "select count(*) as num from region where province=\"".$current_select."\"";
        }
        $result = mysqli_query($link, $sql);
        $data = mysqli_fetch_assoc($result);
    ?>
    <p>
        <h3>Region Info table (Currently <?php echo $data['num']; ?>) regions <?php if($current_select != '-') {echo "by ".$current_select;} ?> in database </h3>
    </p>

    <table cellspacing="0" width="100%">
        <thead>
        <tr>
            <th>Code</th>
            <th>Province</th>
            <th>City</th>
            <th>Latitude</th>
            <th>Longitude</th>
            <th>Elementary_school_count</th>
            <th>Kindergarten_count</th>
            <th>Academy_ratio</th>
            <th>Elderly_population_ratio</th>
            <th>Nursing_home_count</th>
        </tr>
        </thead>
        <tbody>
            <?php
                if($current_select == '-') {
                    $sql = "select * from region";
                } else {
                    $sql = "select * from region where province=\"".$current_select."\"";
                }
                $result = mysqli_query($link,$sql);
                while( $row = mysqli_fetch_assoc($result)  )
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