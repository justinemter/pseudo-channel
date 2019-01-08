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
  	<link rel="shortcut icon" href="https://raw.githubusercontent.com/justinemter/pseudo-channel/master/favicon.ico" type="image/x-icon">
  	<!-- Latest compiled and minified CSS -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

  	<style type="text/css">
  	.channels-selector {
  		width: 124px;
    	margin: 0 auto;
    	text-align: center;
  	}

  	.channels-selector a {
  		margin-top: 3px;
    	font-size: 24px;
  	}

  	.channels-selector .channel-left {
  		float: left;
  	}
  	.channels-selector .channel-right {
  		float: right;
  	}
  	.channels-selector h1 {
  		display: inline-block;
  		margin: 0;
  	}

  	form {
  		margin: 20px 10px;
  		text-align: center;
  	}

  	.schedules-html-paths {
  		display: none;
  	}

  	.heading {
  		text-align: center;
  	}

  	</style>
</head>

<body>
  	<!--[if lte IE 9]>
    <p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
  	<![endif]-->

	<script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
  	<script>window.jQuery || document.write('<script src="js/vendor/jquery-3.3.1.min.js"><\/script>')</script>

	<?php

	$schedules_html_paths = array();

	$dirs = array_filter(glob('*'), 'is_dir');
	
	foreach($dirs as $file) 
	{
		if (strpos($file, 'channel') !== false) {
		    array_push($schedules_html_paths, $file."/schedules/index.html");
		}		
	}

	?>

	<?php

	function updateNowPlayingSchedules() {

	    exec("./generate-html-schedules.sh",$out);
	    /*foreach($out as $key => $value)
		{
		    echo $key." ".$value."<br>";
		}*/
		echo " Update Complete";

	}

	if (isset($_GET['update'])) {

		echo 'Generating new html schedules.';
	    updateNowPlayingSchedules();

	 }

	?>

	<div class="schedules-html-paths" data-results="<?php echo implode(",",$schedules_html_paths); ?>"></div>   

	<h1 class="heading">Multi-Channel</h1>

	<form id="myForm">
	  	<select id="selectNumber">
	    	<option>Choose a Channel</option>
	  	</select>
	  	<a id="gen-schedules" href="?update=true">Generate Now Playing Schedules</a>
	</form>

	<div class="channels-selector">
		<a href="#" class="channel-controls channel-left"><</a>
		<h1></h1>
		<a href="#" class="channel-controls channel-right">></a>
	</div>

	<script type="text/javascript">

		$(document).ready(function(){

			var getBackMyJSON = $('.schedules-html-paths').data('results');
			//console.log(getBackMyJSON);

			var schedules_html_paths = getBackMyJSON.split(',');
			//console.log(schedules_html_paths[0]);

			var select = document.getElementById("selectNumber"); 
			var options = []; 

			for(var j = 0; j < schedules_html_paths.length; j++){
				options.push(schedules_html_paths[j]);
				//console.log(j);
			}

			$('#selectNumber').empty();
			$('#selectNumber').change(function() {

			    $("#iframeHolder").empty();
			    $("#iframeHolder").append('<iframe id="iframe" src="'+$(this).val()+'" width="100%" height="900"></iframe>');

			    //Getting channel number
			    var channelNum = getChannelNumberFromStr($(this).val());

			    $thisItem = $(this);
			    console.log($thisItem.val());
			    $('#selectNumber option').each(function(){
			    	if($(this).val() == $thisItem.val()){
			    		console.log("I made it");
			    		$(this).attr("selected", "selected");
			    	} else {
			    		$(this).removeAttr("selected");
			    		console.log("In here")
			    	}
			    })

			    $(".channels-selector h1").empty().append(channelNum); 

			});

			$.each(options, function(i, p) {
				if(i == 0){
					$('#selectNumber').append($('<option selected="selected"></option>').val(p).html(getChannelNumberFromStr(p)));
				} else {
					$('#selectNumber').append($('<option></option>').val(p).html(getChannelNumberFromStr(p)));
				}
			});

			$(".channel-right").click(function(){

				var nextItem = false;
				for(var i=0; i < $('#selectNumber option').length; i++){

					if(nextItem){

			  			$('#selectNumber option').eq(i).attr('selected', 'selected');
			  			$('#selectNumber').trigger('change');
			  			
			  			break;
			  		} else{

			  		}

					if($('#selectNumber option').eq(i).attr("selected") == "selected") {
						
						if(i != $('#selectNumber option').length -1){
							$('#selectNumber option').eq(i).removeAttr('selected');
						}
			  			nextItem = true;
				    
				  	}
				}
				
				$("#selectNumber option").each(function(i) {
				  	
				});
			});

			$(".channel-left").click(function(){
				var nextItem = false;
				for(var i=$('#selectNumber option').length; i >= 0; i--){

					if(nextItem){
			  			$('#selectNumber option').eq(i).attr('selected', 'selected');
			  			$('#selectNumber').trigger('change');
			  			break;
			  		} else{
			  			//
			  		}

					if($('#selectNumber option').eq(i).attr("selected") == "selected") {
						
						if(i != 0){
				  			$('#selectNumber option').eq(i).removeAttr('selected');
				  		}
			  			nextItem = true;
				    
				  	}
				}

				$("#selectNumber option").each(function(i) {
				  	
				});
			});

			$('#selectNumber').trigger('change');

			function getChannelNumberFromStr(str){
				return str.split('channel_').pop().split('/schedules')[0]; 
			}

		});

	</script>

  	<div id="iframeHolder"></div>
</body>

</html>

