$(document).ready(function() {
	$("#list-search-box").keyup(function() {
		// console.log($(this).val());
		var s_key = $(this).val();
		$(".list-group-item").show();
		$(".order-item").each(function() {
			if($(this).attr('itemdata').search(s_key) == -1)
				$(this).parent('li').hide();
		}); 
	}); 
}); 