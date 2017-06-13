$(document).ready(function() {
	console.log(service_fields);

	var cur_sp_idx, cur_sv_idx, cur_sb_idx; // Current SuperService, Service, SubService indexes
	var docs = [];
	var doc_fields = [
		{'name': 'No', 'type': 'text', 'class':'cell-sm', 'v_name':'no'}, 
		{'name': 'Name', 'type': 'text', 'class':'cell-sm', 'v_name': 'name'}, 
		{'name': 'Description', 'type': 'text', 'class':'cell-lg', 'v_name': 'description'}, 
		{'name': 'Quantity', 'type': 'number', 'class':'cell-sm', 'v_name': 'quantity'}, 
		{'name': 'Unit Price', 'type': 'number', 'class':'cell-sm', 'v_name': 'unit_price'}, 
		{'name': 'Total', 'type': 'hidden', 'class':'cell-sm', 'v_name': 'total'}, 
		{'name': 'Fee', 'type': 'hidden', 'class':'cell-sm', 'v_name': 'fee'}
	]

	$("#superservices").html('');
	for(sp_idx in service_fields) {
		service_field = service_fields[sp_idx];
		var elem = '<li class="nav-item" itemprop='+sp_idx+'> <a class="nav-link" data-toggle="tab" href="#'+sp_idx+'"> '+service_field['name']+' </a> </li>'; 
		$("#superservices").append(elem);
	}
	$("#superservices li:first-child > a").addClass('active');
	$("#superservices li").click(function() {
		setTimeout(refresh_all, 50);
	});

	function refresh_all() {
		cur_sp_idx = parseInt($("#superservices li > a.active").parent().attr("itemprop"));
		$("#services").html('');

		service = undefined;
		for(sv_idx in service_fields[cur_sp_idx]['services']) {
			service = service_fields[cur_sp_idx]['services'][sv_idx];
			var elem = '<option value="'+sv_idx+'" > '+service['name']+' </option>';
			$("#services").append(elem);
		}

		$("#services").change(function() {
			cur_sv_idx = parseInt($("#services").val());
			refresh_service_detail(service_fields[cur_sp_idx]['services'][cur_sv_idx]);
		});
		$("#services").change();

		console.log(service_fields[cur_sp_idx]['services']);

		if(service == undefined)
			$("#services").removeClass('required');
		else 
			$("#services").addClass('required');
	}

	function refresh_service_detail(service) {
		if(service == undefined){
			$("#empty-service").show();
			$("#service_detail .service_detail").hide();
			refresh_subservice(undefined);
			return;
		}

		$("#empty-service").hide();
		$("#service_detail .service_detail").show();

		$("#detail-header").html('<td>'+capitalizeFirstLetter(service['itemName'])+'</td>');
		$("#detail-content").html('');

		for(idx in service['fields']) {
			field = service['fields'][idx];
			var elem = '<tr>';
			elem = elem + '<th> <label for="'+field['v_name']+'">'+capitalizeFirstLetter(field['name'])+'</label> </th>';
			elem = elem + '<td>'; 
			if(field['type'] == 'select') {
				elem = elem + '<select column = "'+field['v_name']+'" class="form-control value-data select required" >'
				values = [];
				if(field['value'] != undefined) {
					values = field['value'].split(',');
				} else {
					values = []
				}
				for(val in values) {
					elem = elem + '<option value="'+values[val]+'" >'+capitalizeFirstLetter(values[val])+'</option>';
				}
				elem = elem + '</select>';
			} else {
				elem = elem + '<input type="'+field['type']+'" column = "'+field['v_name']+'" class="form-control value-data '+field['type']+' required" />';
			}
			elem = elem +'</td>';
			elem = elem + '</tr>';

			$("#detail-content").append(elem);
		}

		$("#detail-subservices").html('');
		for(idx in service['subservices']) {
			subservice = service['subservices'][idx];
			var elem = '<option value="'+idx+'">'+subservice['name']+'</option>';
			$("#detail-subservices").append(elem);
		}

		$("#detail-subservices").change(function() {
			cur_sb_idx = $(this).val();
			refresh_subservice(service_fields[cur_sp_idx]['services'][cur_sv_idx]['subservices'][cur_sb_idx])
		}); 

		$("#detail-subservices").change();

		$(".value-data").blur(function() {
			setTimeout(
				function() {
					$(".autocomplete").parent().remove();
				}, 500) ;
		}); 

		$(".value-data").keydown(function() {
			var field = $(this).attr('column');
			var keyword = $(this).val();
			var all = false;

			$(".autocomplete").parent().remove();

			if(keyword.length < 3) return;
			if($(this).prevAll().length == 0)
				all = true;

			var elem = $(this);

			$.post(
				api_url, 
				{
					'field': field, 
					'keyword': keyword, 
					'all': all, 
					'service_id': service['id'],
					'csrfmiddlewaretoken': csrf
				}, function(r) {
					var data = JSON.parse(r);
					var iN = service_fields[cur_sp_idx]['services'][cur_sv_idx]['itemName']; 
					var fields = service_fields[cur_sp_idx]['services'][cur_sv_idx]['fields']; 
					var style="list-style: none;"+
						    "text-align: left;" +
						    "position: absolute;" +
						    "background: #fff;" +
						    "box-shadow: 1px 2px 7px 1px #776;" +
						    "display: inline-block;" +
						    "left: 33.333%;" +
						    "margin-top: 30px; " + 
						    "cursor: pointer;" + 
						    "width: 58.6666%;";
					var dropdown = $("<ul style='"+style+"' > </ul>");
					for(idx in data[iN]) {
						var elm = "<li class='autocomplete' idx='"+idx+"'>" + data[iN][idx][field] + "</li>";
						dropdown.append(elm);
					}
					elem.nextAll().remove();
					if(data[iN].length > 0)
						dropdown.insertAfter(elem);

					$(".autocomplete").click(function() {
						var idx = parseInt($(this).attr("idx"));
						for(fid in fields) {
							$("*[column='"+fields[fid]['v_name']+"'").val(data[iN][idx][fields[fid]['v_name']]);
						}
						if(data['location'] != undefined) {
							$("#receiver-name").val(data['location']['name']);
							$("#receiver-address").val(data['location']['address']);
							$("#receiver-postcode").val(data['location']['post']);
							$("#receiver-country").val(data['location']['country']); 
							$("#receiver-email").val(data['location']['email']);
							$("#receiver-phone").val(data['location']['phone']);
							$("#receiver-fax").val(data['location']['fax']);
						}
						$(this).parent().remove();
					}); 

				} ); 
		}); 

	}

	function refresh_subservice(subservice) {
		docs = [];
		if(subservice == undefined) {
			refresh_documents();
			return; 
		}
		for(idx in subservice['checklist']) {
			var item = {}
			sb_item = subservice['checklist'][idx]
			for(idx in doc_fields) {
				field = doc_fields[idx];
				if(field['v_name'] == 'total')
					continue;
				item[field['v_name']] = sb_item[field['v_name']];
			}
			item['total'] = parseFloat(item['unit_price']) * parseFloat(item['quantity']);
			item['delete'] = false;
			docs.push(item);
		}
		refresh_documents();
	}

	function refresh_documents() {
		$("#documents_header").html('');
		for(idx in doc_fields) {
			field = doc_fields[idx];
			var elem = '<th class="'+field['class']+'">'+field['name'] + '</th>';
			$("#documents_header").append(elem);
		}
		$("#documents_header").append('<th class="cell-sm">-</th>');
		$("#documents_body").html('');
		for(d_idx in docs) {
			doc = docs[d_idx];
			var elem = '<tr>';
			for(idx in doc_fields) {
				field = doc_fields[idx];
				elem = elem + '<td class="'+field['class']+'"  title="' + doc[field['v_name']] + '" >' + doc[field['v_name']] + '</td>';
			}
			if(doc['delete'])
				elem = elem + '<td > <span row="'+d_idx+'" class="fa fa-trash-o remove-row"> </span> </td>';
			else 
				elem = elem + '<td > <span row="'+d_idx+'" class="fa fa-ban"> </span> </td>';
			elem = elem + '</tr>';
			$("#documents_body").append(elem);
		}
		var elem = '<tr id="new_doc">';
		for(idx in doc_fields) {
			field = doc_fields[idx];
			elem = elem + '<td class="'+field['class']+'"> <input class="form-control" type="'+field['type']+'" itemprop = "'+field['v_name']+'" /></td>';
		}
		elem = elem + '<td > -</td>';
		elem = elem + '</tr>';
		$("#documents_body").append(elem);
		$("#documents_body").append(' <tr> <td colspan="4"> </td> <td colspan="2" class="add_document"> <button id="add_document" class="btn btn-primary" > Add Document </button> </td> <td colspan="2"> </td> </tr>') 

		$("#add_document").click(function() {
			var item = {};
			for(idx in doc_fields) {
				field = doc_fields[idx];
				if(field['v_name'] == 'total' || field['v_name'] == 'fee')
					continue;
				item[field['v_name']] = $("#new_doc input[itemprop='"+field['v_name']+"'").val();
				if(item[field['v_name']] == undefined || item[field['v_name']] == 0 || parseFloat(item[field['v_name']]) < 0) {
					$("#new_doc input[itemprop='"+field['v_name']+"'").focus();
					return;
				}
			}
			item['total'] = parseFloat(item['unit_price']) * parseFloat(item['quantity']);
			item['delete'] = true;
			item['fee'] = 1;
			docs.push(item);
			refresh_documents();
		}); 

		$("#documents_body .remove-row").click(function() {
			row = parseInt($(this).attr('row'));
			docs.splice(row, 1);
			refresh_documents();
		}); 

	}

	refresh_documents();

	refresh_all();

	function validateForm() {
		$("*.required").each(function() {
			console.log(this);
			console.log($(this).val());
			if($(this).val() == undefined || $(this).val() == '') {
				var elem = this;
				$('html, body').animate({
					scrollTop: $(elem).offset().top - 70
				}, 700);
				setTimeout(function() {
					$(elem).focus();
				}, 920);
				return false;
			}
		});
		console.log(docs);
		console.log(docs.length);
		if(docs.length == 0) {
			$("div.documents table").focus();
			return false;
		}
		return true;
	}

	$("#submit_order").click(function() {

		if(!validateForm())
			return false;

		var data = {};
		data['sender'] = {};
		data['sender']['address'] = $("#sender-address").val();
		data['sender']['postcode'] = $("#sender-postcode").val();
		data['sender']['country'] = $("#sender-country").val();
		data['sender']['email'] = $("#sender-email").val();
		data['sender']['phone'] = $("#sender-phone").val();
		data['sender']['fax'] = $("#sender-fax").val();

		data['receiver'] = {};
		data['receiver']['name'] = $("#receiver-name").val();
		data['receiver']['address'] = $("#receiver-address").val();
		data['receiver']['postcode'] = $("#receiver-postcode").val();
		data['receiver']['country'] = $("#receiver-country").val();
		data['receiver']['email'] = $("#receiver-email").val();
		data['receiver']['phone'] = $("#receiver-phone").val();
		data['receiver']['fax'] = $("#receiver-fax").val();

		data['service'] = {};
		data['service']['super'] = {};
		data['service']['super']['name'] = service_fields[cur_sp_idx]['name'];
		data['service']['service'] = {};
		if(service_fields[cur_sp_idx]['services'][cur_sv_idx] != undefined) {
			data['service']['service']['name'] = service_fields[cur_sp_idx]['services'][cur_sv_idx]['name'];
			itemName = data['service']['service']['itemName'] = service_fields[cur_sp_idx]['services'][cur_sv_idx]['itemName'];
			data['service']['service'][itemName] = {};
			for(idx in service_fields[cur_sp_idx]['services'][cur_sv_idx]['fields']) {
				field = service_fields[cur_sp_idx]['services'][cur_sv_idx]['fields'][idx];
				data['service']['service'][itemName][field['v_name']] = {};
				data['service']['service'][itemName][field['v_name']]['name'] = field['name'];
				data['service']['service'][itemName][field['v_name']]['value'] = $("*[column='"+field['v_name']+"'").val();
			}
			data['service']['subservice'] = {};
			if(service_fields[cur_sp_idx]['services'][cur_sv_idx]['subservices'][cur_sb_idx] != undefined)
				data['service']['subservice']['name'] = service_fields[cur_sp_idx]['services'][cur_sv_idx]['subservices'][cur_sb_idx]['name'];
		}
		data['documents'] = docs;

		console.log(data);

		data = JSON.stringify(data);
		$("#order-data").val(data);
		$("#order-form").submit();

	}); 


});
