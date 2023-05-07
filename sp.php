<!DOCTYPE html>
<html>
<head>
	<title>URL Checker</title>
	<style>
		body {
			background-color: #f2f2f2;
			font-family: Arial, sans-serif;
		}
 		h1 {
			color: #4d4d4d;
			text-align: center;
			margin-top: 50px;
		}
 		form {
			margin: 0 auto;
			display: flex;
			flex-direction: column;
			align-items: center;
			margin-top: 50px;
			padding: 20px;
			background-color: #ffffff;
			box-shadow: 0px 0px 10px 0px rgba(0,0,0,0.2);
			border-radius: 10px;
			width: 50%;
			min-width: 400px;
		}
 		label {
			font-size: 16px;
			font-weight: bold;
			color: #4d4d4d;
			margin-bottom: 10px;
		}
 		textarea {
			width: 100%;
			padding: 10px;
			border-radius: 5px;
			border: 1px solid #cccccc;
			resize: none;
			height: 200px;
			margin-bottom: 20px;
			font-size: 16px;
			color: #4d4d4d;
		}
 		input[type="submit"] {
			background-color: #4d4d4d;
			color: #ffffff;
			padding: 10px 20px;
			border-radius: 5px;
			border: none;
			font-size: 16px;
			cursor: pointer;
			transition: background-color 0.3s ease;
		}
 		input[type="submit"]:hover {
			background-color: #333333;
		}
 		.result {
			margin: 0 auto;
			width: 50%;
			min-width: 400px;
			background-color: #ffffff;
			padding: 20px;
			margin-top: 20px;
			box-shadow: 0px 0px 10px 0px rgba(0,0,0,0.2);
			border-radius: 10px;
			max-height: 300px;
			font-size: 16px;
			color: #4d4d4d;
			overflow: auto;
			text-align: center;
			display: none;
		}
 		.result p {
			margin: 0;
			padding: 5px;
		}
 		.result .alive {
			background-color: #c6efce;
			color: #4d4d4d;
		}
 		.result .dead {
			background-color: #f8cecc;
			color: #4d4d4d;
		}
	</style>
</head>
<body>
	<h1>URL Checker</h1>
	<form method="POST" onsubmit="showResult(); return false;">
		<label>Enter URLs (one per line):</label>
		<textarea name="urls" id="urls" placeholder="https://example.com&#10;https://google.com"></textarea>
		<input type="submit" value="Check">
	</form>
	<div class="result" id="result"></div>
	<script>
		function showResult() {
			var urls = document.getElementById('urls').value.trim().split('\n');
			var resultDiv = document.getElementById('result');
			resultDiv.innerHTML = '';
			resultDiv.style.display = "block";
			urls.forEach(function(url) {
				url = url.trim();
				if (url !== '') {
					var xhr = new XMLHttpRequest();
					xhr.open('HEAD', url, true);
					xhr.onload = function() {
						if (xhr.status === 200) {
							resultDiv.innerHTML += '<p class="alive">' + url + ' is alive</p>';
						} else {
							resultDiv.innerHTML += '<p class="dead">' + url + ' is dead</p>';
						}
					};
					xhr.onerror = function() {
						resultDiv.innerHTML += '<p class="dead">' + url + ' is dead</p>';
					};
					xhr.send();
				}
			});
		}
	</script>
</body>
</html>
