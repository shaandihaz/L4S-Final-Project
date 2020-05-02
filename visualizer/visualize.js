
function parse(raw_json) {
	const json = JSON.parse(raw_json);
	const numActors = json["numActors"];
	const numProps = json["numProps"];
	const numScenes = json["numScenes"];
	const sceneData = json["sceneData"];
	console.log("number of actors: " + numActors);
}

$("#file").on("change", function() {
	const file = $("#file").prop("files")[0];
	const fr = new FileReader();
	fr.onload = function() {
		console.log(fr.result);
		parse(fr.result);
	};
	fr.readAsText(file);
});
