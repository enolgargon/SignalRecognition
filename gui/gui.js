var frame = null;
var images = null;

var update = () => {
	$.ajax({
		type: 'GET',
		url: 'http://127.0.0.1:5000/current-frame',
		dataType: 'json',
		crossDomain: true,
		success: data => {
			$("#frame").attr('src', `file:///home/enolgargon/images/${data.frame}.png`)
		}
	});

	$.ajax({
		type: 'GET',
		url: 'http://127.0.0.1:5000/current-signals',
		dataType: 'json',
		crossDomain: true,
		success: data => {
			$("#signals").empty();
			data.forEach(element => $("#signals").append(`<img src="file:///home/enolgargon/icon/${element.code.toString().padStart(2, 0)}.png" />`))
		}
	});
};

setInterval(update, 500);
