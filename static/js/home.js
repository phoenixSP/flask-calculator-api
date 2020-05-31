$(document).ready(function(){
			// sending a connect request to the server.
			var socket = io.connect('127.0.0.1:5000/');
			// console.log("Input operation"+$("#operation").val())
			$("#operation_form").submit(function(){
    			console.log("Doing after subkmit")
    			socket.emit('/new_operation/', {'operation': $("#operation").val()})	
			});
			socket.on('notification', function(msg){	
    				console.log( "Client side"+msg );
    				$("#notification_holder").text(msg);
    				
    				// $("#notification_area").replaceWith('<h3>'+msg+'</h3>');
    				});	
    				
    		socket.on('result', function(msg){
        		console.log("Operation Client side"+msg);
        		// $("#result").text("The result is: "+msg);
        		
    		});
        }); 