var labels, canvas_wrapper;

var ImageCanvas = function(canvas, image) {
	var context, mult;
	
	canvas.width = image.width;
	canvas.height = image.height;
	
	context = canvas.getContext("2d");
	context.canvas.width = image.width;
	context.canvas.height = image.height;
	
	context.strokeStyle = "pink";
	context.lineWidth = "3";
	context.fillStyle = "Crimson";
	context.font = "14px Arial";
	
	context.drawImage(image, 0, 0);
	
	this.draw_box = function(xMin, xMax, yMin, yMax) {
		context.beginPath();
		context.rect(xMin, yMin, xMax - xMin, yMax - yMin);
		context.stroke();
	};
	
	this.label_box = function(label, xMin, xMax, yMin, yMax) {
		context.fillText(label, xMin, yMin);
	};
	
	this.refresh = function() {
		context.clearRect(0, 0, image.width, image.height);
		context.drawImage(image, 0, 0);
	};
	
	this.click = function(x, y) {};
	this.mousemove = function(x, y) {};
	
	this.get_mult = function() {
		return image.width / canvas.scrollWidth;
	}
	
	canvas.onclick = (function(e) {
		var mult = this.get_mult();
		var x = mult * e.offsetX;
		var y = mult * e.offsetY;
		
		this.click(x, y);
	}).bind(this);
	
	canvas.onmousemove = (function(e) {
		var mult = this.get_mult();
		var x = mult * e.offsetX;
		var y = mult * e.offsetY;
		
		this.mousemove(x, y);
	}).bind(this);
}

function draw_labels() {
	for (var i = 0; i < labels.length; i++)
		canvas_wrapper.draw_box(labels[i].xMin, labels[i].xMax, labels[i].yMin, labels[i].yMax);
	
	for (var i = 0; i < labels.length; i++)
		canvas_wrapper.label_box(i + ": " + labels[i].name, labels[i].xMin, labels[i].xMax, labels[i].yMin, labels[i].yMax);
}

function add_button(id, label) {
	var record = $(' \
		<div class="list-group-item"> \
			<div class="input-group"> \
				<span class="input-group-addon">' + id + '</span> \
				<text style="background-color:#E5E7E9;" class="form-control custom-control" style="resize:none">' + label + '</text> \
				 \
				<span class="input-group-btn"> \
					<button class="btn btn-danger" type="button">-</button> \
				</span> \
			</div> \
		</div> \
	');
	
	record.find("button").click(function (e) {
		labels.splice(id, 1);
		reload_all();
	});
	
	$("#labels_list").append(record);
}

function add_label(xMin, xMax, yMin, yMax) {
	var label = $('#class_name').text();
	var id = labels.length;
	
	labels.push({
		name: label,
		xMin: xMin,
		xMax: xMax,
		yMin: yMin,
		yMax: yMax
	});
	
	add_button(id, label);
}

function reload_all() {
	$("#labels_list").empty();
	$("#labels_list").append($('<div class="list-group-item">Your Labels</div>'));
	
	for (var i = 0; i < labels.length; i++)
		add_button(i, labels[i].name);
	
	canvas_wrapper.refresh();
	draw_labels();
}

function send_data() {
	
	if (labels.length == 0) {
		alert("You need to add at least one label");
		return;
	}
	
	if (!confirm("Are you sure?"))
		return;
	
	$.ajax({
		url : "/api/labeled_upload",
		type: "POST",
		data: JSON.stringify({labels: labels}),
		dataType: "json",
		contentType: "application/json"
	}).always(function (data) {location.reload();});
}

$(window).on("load", function() {
	
	$("#send_button").click(send_data);
	
	$("#label_dropdown").on("click", "li", function (e) {
		var label = $(this).find('a').text();
		$('#class_name').text(label);
	});
	
	canvas_wrapper = new ImageCanvas($("#canvas").get(0), $("#hide_img").get(0));
	labels = [];
	
	reload_all();
	
	
	var clicked = false;
	var xMin, xMax, yMin, yMax;
	
	canvas_wrapper.click = function(x, y) {
		
		if (!clicked) {
			xMin = xMax = x;
			yMin = yMax = y;
			
			canvas_wrapper.mousemove = function(_x, _y) {
				var temp_xMin = Math.min(x, _x);
				var temp_xMax = Math.max(x, _x);
				var temp_yMin = Math.min(y, _y);
				var temp_yMax = Math.max(y, _y);
				
				canvas_wrapper.refresh();
				canvas_wrapper.draw_box(temp_xMin, temp_xMax, temp_yMin, temp_yMax);
				draw_labels();
			};
		} else {
			canvas_wrapper.mousemove = function (_x, _y) {};
			
			xMin = Math.min(xMin, x);
			xMax = Math.max(xMax, x);
			yMin = Math.min(yMin, y);
			yMax = Math.max(yMax, y);
			
			add_label(xMin, xMax, yMin, yMax);
			canvas_wrapper.refresh();
			draw_labels();
		}
		
		clicked = !clicked;
	};
});