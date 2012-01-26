function change_color(active_color) {
		$(".renkduzeni").css("backgroundColor",active_color);
		$("h3").css("color",active_color);
		$("#id_color").val(active_color);
	}
	
function arkadaslikIstegi(kullaniciAdi) {
	$.get(
	"ajax.php",
	{"act":"ark",kullanici: kullaniciAdi,"nocache":Math.random},
	function(Cevap){
    	$('#info').html(Cevap).fadeIn("slow");
	}
);


}

function rTrue() {
	// hatasiz cool olmaz...
	return true;
}
