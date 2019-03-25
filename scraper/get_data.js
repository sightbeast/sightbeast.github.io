x = 10

jQuery.noConflict();
$=jQuery;

function clearElement(el) {
	$(el).find('.all')[0].click()
}

function loadswag(el, callback) {
	console.log('jQuery injected')
	console.log('moving on')
	$("#sneakers").find('.all').click()
	limit = parseInt($(".gauge-value")[0].innerHTML)
	console.log(limit)
	limit = Math.min(1000, limit)
	intervalID = setInterval(function () {
		l = $(el).find("tbody").children('tr');
		$(".button.button-block.button-white").click();
		console.log(x, l.length, l)
		while(l.length >= $(el).find("tbody").children('tr').length) {
			l = $(el).find("tbody").children('tr')
		}
		x = l.length
		console.log(x, l);
		if (x >= limit || x >= 1000) {
			window.clearInterval(intervalID);
			callback();
		}
	}, 1000);
}

function download(filename, text, el, callback) {
	var element = document.createElement('a');
	element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
	element.setAttribute('download', filename);

	element.style.display = 'none';
	document.body.appendChild(element);

	element.click();

	document.body.removeChild(element);
	callback();
}

function writeCSV(el, name, element) {
	//clearElement(element);
	loadswag(el, function() {
		finalSizes = []
		console.log($(el).find("tbody"))
		$(el).find("tbody").children('tr').each(function () {
			temp = []
		    $(this).children('td').each(function () {
				console.log($(this)[0].outerText)
				temp.push($(this)[0].outerText)
		    });
			finalSizes.push(temp);
		});
		rows = finalSizes
		console.log(rows)
		//csvContent = "data:text/csv;charset=utf-8,\n";
		csvContent = 'Size,Price,Number Available\n'
		rows.forEach(function(rowArray){
	   		let row = rowArray.join(",");
	   		csvContent += row + "\r\n";
		});
		console.log(name)
		download(name+'.csv', csvContent, element, function() {console.log(csvContent);console.log(element);$( "body" ).append( "<p id='fuckingloaded'></p>" );}) 
	});
}