<!doctype html>
<html class="no-js" lang="">

<head>
  <meta charset="utf-8">
  <meta http-equiv="x-ua-compatible" content="ie=edge">
  <title></title>
  <meta name="description" content="">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <link rel="manifest" href="site.webmanifest">
  <link rel="apple-touch-icon" href="icon.png">
  <!-- Place favicon.ico in the root directory -->

  <link rel="stylesheet" href="css/normalize.css">
  <link rel="stylesheet" href="css/main.css">
</head>

<body>
  	<!--[if lte IE 9]>
    <p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
  	<![endif]-->

	<script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
  	<script>window.jQuery || document.write('<script src="js/vendor/jquery-3.3.1.min.js"><\/script>')</script>

	<?php

	$cur_dir = explode('\\', getcwd());
	//echo $cur_dir[count($cur_dir)-1] . "<br />";

	$schedules_html_paths = array();
	$dir = $cur_dir[count($cur_dir)-1] . "/*";
	foreach(glob(basename($dir) . '/schedules' , GLOB_ONLYDIR) as $file) 
	{
		$dirs = array_filter(glob($file), 'is_dir');
		//echo $file."/index.html" . "<br />";
		array_push($schedules_html_paths, $file."/index.html");
	}

	//print_r($schedules_html_paths)

	?>

	<div class="schedules-html-paths" data-results="<?php echo implode(",",$schedules_html_paths);; ?>"></div>   

	<script type="text/javascript">
		var getBackMyJSON = $('.schedules-html-paths').data('results');
		//console.log(getBackMyJSON);

		var schedules_html_paths = getBackMyJSON.split(',');
		//console.log(schedules_html_paths[0]);
	</script>

	<form id="myForm">
	  	<select id="selectNumber">
	    	<option>Choose a Channel</option>
	  	</select>
	</form>

	<script type="text/javascript">
		var select = document.getElementById("selectNumber"); 
		var options = []; 

		for(var j = 0; j < schedules_html_paths.length; j++){
			options.push(schedules_html_paths[j]);
			//console.log(j);
		}

		//$('#selectNumber').empty();
		$.each(options, function(i, p) {
		    $('#selectNumber').append($('<option></option>').val(p).html(p));
		});

		$('#selectNumber').change(function() {
		     console.log($(this).val())
		     $("#iframeHolder").empty();
		     $("#iframeHolder").append('<iframe id="iframe" src="'+$(this).val()+'" width="100%" height="900"></iframe>');
		});
	</script>

  	<div id="iframeHolder"></div>
</body>

</html>

