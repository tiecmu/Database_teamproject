<?php
    $link = mysqli_connect("localhost","wotjd2979", "123456", "k_covid19");
    if( $link === false )
    {
        die("ERROR: Could not connect. " . mysqli_connect_error());
    }
   
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
    <h1 style="text-align:center"> Patient Search </h1>
    <hr style = "border : 5px solid yellowgreen">

    <?php
	$action = '';
	if(isset($_POST['action']))$action = $_POST['action'];
        
        $current_search = NULL;
	if($action == 'form_submit') {
            $current_search = $_POST['patient_id'];
            echo '<xmp>';
            
            if($current_search == NULL){}
            else {
                echo 'Searching patient information by '.$current_search;
            }
            echo '</xmp>';
	}
    ?>
    <form method="post" action="<?=$_SERVER['PHP_SELF']?>">
	<input type="hidden" name="action" value="form_submit" />
        Put Patient_id : <input name="patient_id">
        </input>
  	<input type="submit" value="sumbit" />
    </form>
    
    <?php
        if($current_search != NULL) {
            $sql = "select count(*) as num from patientinfo where patient_id=\"".$current_search."\"";
            $result = mysqli_query($link, $sql);
            $data = mysqli_fetch_assoc($result);    
        }
    ?>
    
    <p>
        <h3>Patient Info table (Currently <?php if($current_search != NULL){ echo $data['num']; } ?>) patients <?php if($current_search != NULL) {echo "in Hospital Id : ".$current_search;} ?> in database </h3>
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
            <th>released_date	</th>
            <th>deceased_date</th>
            <th>state</th>
            <th>Hospital_id</th>
        </tr>
        </thead>
        <tbody>
            <?php
               
                $sql = "select * from patientinfo where patient_id=\"".$current_search."\"";
                
                $result = mysqli_query($link,$sql);
                while( $row = mysqli_fetch_assoc($result)  )
                {
                    print "<tr>";
                    
                    foreach($row as $key => $val)
                    {
                        if($key!="hospital_id")
                        { 
                            print "<td>" . $val . "</td>";
                        }
                        else {
                            print "<td><a href='search_patient_id_with_map.php?hospital_id=".$val."'>".$val."</a></td>";
                        }
                    }
                    print "</tr>";
                }
            ?>
        </tbody>
    </table>

    <?php
	$lat=0;
	$lng=0;
        $hospital_id = NULL;
        if(isset($_GET['hospital_id'])) {
            $hospital_id = $_GET['hospital_id'];

	$sql = "select Hospital_latitude, Hospital_longitude from hospital where hospital_id=$hospital_id";
                $result = mysqli_query($link,$sql);
                while( $row = mysqli_fetch_assoc($result)  )
                {
                    print "<tr>";
		
                    foreach($row as $key => $val)
                    {
		#print "<td>" . $val . " </td>";
		if($lat==0){$lat=$val;}
		else{$lng=$val;}
		}
                    print "</tr>";
                }
        }
    ?>
<div id="map" style="width:100%; height: 100vh;"></div>
    <script async defer src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCgfsIMFbCsHb7D8fCE5wrWGJMGpOQBiEE&callback=initMap&region=kr"></script>
    <script>
        var lat1 =0;
        var lat1 = <?= $lat ?>;
        var lng1 = <?= $lng ?>;
        if(lat1!=0){
            function initMap() {
                var hospital = { lat: lat1 ,lng: lng1 };
                var map = new google.maps.Map(
                    document.getElementById('map'), {
                    zoom: 17,
                    center: hospital
                });
                var marker = new google.maps.Marker({position: hospital, map: map});
            }
        }
    </script>
</body>