window.onload = function generate_unique_ids_for_posts(){
	let unique_ids = [], empty_string = '';
	let links = document.querySelectorAll('#comment_link');
	let comment_sections = document.querySelectorAll('#comment_section');
	let index = 0;
	// Creating unique ids for <a> tags and comment sections
	for(let i = 0;i < links.length; i++){
		links[i].id = index;
		comment_sections[i].id = empty_string.concat('div_',index.toString());
		index++;
	}
} 


function get_commentbox(id){
	let a_link = document.getElementById(id), comment_section;
	comment_section = document.getElementById("div_" + a_link.id.toString()) 
	if(comment_section.style.display == "none"){
		comment_section.style.display = "block";
	}else{
		comment_section.style.setProperty("display", "none", "important");
	}
}


