$(window).on("load", function() {
	
	$(".non-active").each(function (index) {
		$(this).attr("disabled", "disabled");
		$(this).css("cursor", "default");
	});
	
	
	var highestBox = 0;
	
	$('#inference_form .btn').each(function(){  
		highestBox = Math.max(highestBox, $(this).height());
	});
	
	$('#inference_form .btn').height(highestBox);
	
	
	$("#input_img").on("change", function(e) {
		["inference_submit_button", "label_submit_button"].forEach(function (id) {
			$("#" + id).removeAttr("disabled");
			$("#" + id).css("cursor", "pointer");
		});
	});
	
	$("#inference_submit_button").click(function(e) {
		
		$("#modalWindow").modal("show");
		
		var data = new FormData($("#inference_form").get(0));
		
		$.ajax({
			url : "/api/inference",
			type: "POST",
			data: data,
			cache: false,
			contentType: false,
			processData: false
		})
		.done(function(data) {
			$("#labeled_img").attr("src", data["url"]);
		})
		.fail(function(data) {
			alert("Oops, some error occured, we are sorry...");
		})
		.always(function(data) {
			$("#modalWindow").modal("hide");
		});
		
		e.preventDefault();
	});
});