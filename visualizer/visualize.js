let numActors;
let numProps;
let numScenes = 1; // default to 1 so the initial error handling of the next button works
let sceneData;

let currScene = 0;

function parse(raw_json) {
	// empty the containers
	$(".actorpropContainer").empty();

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
	const carryOn = currScene["carryOn"];
	const carryOff = currScene["carryOff"];

	// appending actors to CENTER
	const actors = currScene["actors"];
	actors.forEach(function(a) {
		appendActor(a, "CENTER", carryOn, carryOff);
	});

	// appending leftActors to LEFT
	const actorsLeft = currScene["leftActors"];
	actorsLeft.forEach(function(a) {
		appendActor(a, "LEFT", carryOn, carryOff);
	});

	// appending rightActors to RIGHT
	const actorsRight = currScene["rightActors"];
	actorsRight.forEach(function(a) {
		appendActor(a, "RIGHT", carryOn, carryOff);
	});

	// appending props to CENTER
	const props = currScene["props"];
	props.forEach(function(p) {
		appendProp(p, "CENTER");
	});

	// appending leftProps to LEFT
	const propsLeft = currScene["leftProps"];
	propsLeft.forEach(function(p) {
		appendProp(p, "LEFT");
	});

	// appending rightProps to RIGHT
	const propsRight = currScene["rightProps"];
	propsRight.forEach(function(p) {
		appendProp(p, "RIGHT");
	});

	// initialize all tooltips
	$('[data-toggle="tooltip"]').tooltip();
}

function appendActor(name, position, carryOn, carryOff) {

	// will remain blank, and thus not be added to the elt,
	// if this actor will not be carrying any props
	let tooltip = "";

	if (carryOn[name]) {
		const title = `${name} will carry on ${carryOn[name]}`
		tooltip = `data-toggle="tooltip" data-placement="top" title="${title}"`
	}

	if (carryOff[name]) {
		const title = `${name} will carry off ${carryOff[name]}`
		tooltip = `data-toggle="tooltip" data-placement="top" title="${title}"`
	}

	// constructs the selector for the actor container
	selector = `#${position} .actorpropContainer`
	// constructs the label for this actor
	const n = name.charAt(name.length - 1);
	// constructs the new element
	newElt = `
	<div class="btn btn-danger btn-circle btn-lg" ${tooltip}>
		<span>A${n}</span>
	</div>`
	// appends the element to the container
	$(selector).append(newElt);
}

function appendProp(name, position) {
	// constructs the selector for the actor container
	selector = `#${position} .actorpropContainer`
	// constructs the label for this actor
	const n = name.charAt(name.length - 1);
	// constructs the new element
	newElt = `
	<div class="btn btn-primary btn-circle btn-lg">
		<span>P${n}</span>
	</div>`
	// appends the element to the container
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
			$(".actorpropContainer").empty();
			currScene = currScene - 1;
			$("#sceneNum").html(`Scene ${currScene}`);
			displayScene(currScene);
		}
	});

	$("#nextButton").on("click", function(){

		if (currScene == numScenes - 1) {
			alert("There's no next scene!");
		} else {
			$(".actorpropContainer").empty();
			currScene = currScene + 1;
			$("#sceneNum").html(`Scene ${currScene}`);
			displayScene(currScene);
		}
	});
});
