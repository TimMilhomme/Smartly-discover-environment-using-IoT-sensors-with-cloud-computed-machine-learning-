  function lv_init() {
    var socket = io.connect('http://'+document.domain+':'+location.port);
    socket.on('connect', function(msg) {
      socket.emit('my event', {data: 'client connected!'});
    });
    socket.on('rsp', function(msg) {
      console.log(msg);
    });
    socket.on('message', function(msg) {
      //console.log(msg.data);
      // Plot the data using D3.js (aka Plotly)
      var trace1 = {
				mode: 'lines',
				name: 'Distance (mm) ',
				line: {color: 'peru'},
				type: 'scatterpolar'
      };
      var obj = JSON.parse(msg.data);
      trace1.r = Object.values(obj);
      trace1.theta = Object.keys(obj);
      var layout = {
				title: 'YDLIDAR Distance Measurements',
				font: {
					family: 'Arial, sans-serif;',
					size: 12,
					color: '#000'
				},
				polar: {
					angularaxis: {
						visible: true,
						rotation: 0,
						direction: 'clockwise'
					}
				},
				showlegend: true,
      };
      // Make sure it's a new plot with each measurement!
      Plotly.newPlot('chart',[trace1],layout,{showSendToCloud:true});
      // Update the data rate
      document.getElementById('rate').innerHTML = msg.time;
    });
  }
