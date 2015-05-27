<?php
   class MyDB extends SQLite3
   {
      function __construct()
      {
         $this->open('gstring-sql.db');
      }
   }
   $db = new MyDB();
   if(!$db){
      echo $db->lastErrorMsg();
   } else {
     // echo "Opened database successfully\n";
      
   }

   $sql =<<<EOF
      SELECT * from gpsdata order by id desc limit 1;
EOF;

   $ret = $db->query($sql);
   while($row = $ret->fetchArray(SQLITE3_ASSOC) ){
     	$arr = array('id'=>$row['id'], 'msgType'=>$row['msgType'], 
		'imei'=>$row['imei'], 'validFix'=>$row['validFix'],
		'gpsTime'=>$row['gpsTime'], 'lat'=>$row['lat'],
		'ns'=>$row['ns'], 'lon'=>$row['lon'], 'ew'=>$row['ew'],
		'sog'=>$row['sog'], 'cog'=>$row['cog'], 'sats'=>$row['sats'],
		'hdop'=>$row['hdop']);
	echo json_encode($arr);
	
   }
 //  echo "Operation done successfully\n";
   $db->close();
?>
