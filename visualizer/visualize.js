let numActors;
let numProps;
let numScenes = 1; // default to 1 so the initial error handling of the next button works
let sceneData;

let currScene = 0;

function parse(raw_json) {
	const json = JSON.parse(raw_json);
	numActors = json["numActors"];
	numProps = json["numProps"];
	numScenes = json["numScenes"];
	sceneData = json["sceneData"];
	// TODO: make next and previous buttons appear

	// defaults to displaying the first scene
	displayScene(currScene);
	$("#sceneNum").html(`Scene ${currScene}`);
}

function displayScene(sceneNumber) {
	const key = "Scene " + sceneNumber;
	const currScene = sceneData[key];
	// currScene["carryOff"]
	// currScene["carryOn"]
	// currScene["props"]
	const actors = currScene["actors"];
	actors.forEach(function(a) {
		appendActor(a, "CENTER");
	});

	const actorsLeft = currScene["leftActors"];
	actorsLeft.forEach(function(a) {
		appendActor(a, "LEFT");
	});

	const actorsRight = currScene["rightActors"];
	actorsRight.forEach(function(a) {
		appendActor(a, "RIGHT");
	});

	// currScene["leftActors"]
	// currScene["rightActors"]
	// currScene["leftProps"]
	// currScene["rightProps"]
}

function appendActor(name, position) {

	selector = `#${position} .actorContainer`

	const n = name.charAt(name.length - 1);

	newElt = `
	<div class="btn btn-warning btn-circle btn-lg">
		<span>A${n}</span>
	</div>`

	$(selector).append(newElt);
}


$(document).ready(function() {

	// instantiates a FileReader
	const fr = new FileReader();

	// sets the handler for when the filereader loads a file
	fr.onload = function() {
		// call the parse function above to parse the json
		parse(fr.result);
	};

	// adds a handler to the file input
	$("#file").on("change", function() {

		// gets the file that the user inputted
		const file = $("#file").prop("files")[0];

		// read the file (this triggers the onload handler above)
		fr.readAsText(file);
	});

	$("#prevButton").on("click", function(){
		if (currScene == 0) {
			alert("There's no previous scene!");
		} else {
			$(".actorContainer").empty();
			currScene = currScene - 1;
			$("#sceneNum").html(`Scene ${currScene}`);
			displayScene(currScene);
		}
	});

	$("#nextButton").on("click", function(){

		if (currScene == numScenes - 1) {
			alert("There's no next scene!");
		} else {
			$(".actorContainer").empty();
			currScene = currScene + 1;
			$("#sceneNum").html(`Scene ${currScene}`);
			displayScene(currScene);
		}
	});
});
