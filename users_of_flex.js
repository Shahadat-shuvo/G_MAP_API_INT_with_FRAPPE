// Copyright (c) 2023, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Users of FLEX', {
	street_address: function(frm) {
		let inputs = frm.doc.street_address;
		console.log('Shuvo');
		// Server call for retrieve available nearest streets (maximum 5 street will be fetch)
		frappe.call({
			method: 'frappe.core.doctype.users_of_flex.gmap_api.places',
			args: {
				'user_input': inputs,
			},
			callback: function(r) {
				let responses = r.message; 
				if (responses) {
		
					frm.fields_dict.city.set_data(responses);
					
				} else {
					frm.set_value('city', '');
				}
								
				
				console.log(responses);
				
					}
				});
	}, 
	city: function(frm) {
		let usr_inp = frm.doc.city;

		// Set State Name 
			if (usr_inp.includes('VIC')) {
				frm.set_value('state', 'Victoria');
			} else if (usr_inp.includes('NSW')) {
				frm.set_value('state', 'New South Wales');
			} else if (usr_inp.includes('QLD')) {
				frm.set_value('state', 'Queensland');
			} else if (usr_inp.includes('WA')) {
				frm.set_value('state', 'Western Australia');
			} else if (usr_inp.includes('SA')) {
				frm.set_value('state', 'South Australia');
			} 
			else {
				frm.set_value('state', 'Tasmania');
			}

			// Server call for retrieve Post_code according to city

			frappe.call({
				method: 'frappe.core.doctype.users_of_flex.gmap_api.mapess',
				args: {
					'usr_inp': usr_inp
				},
				callback:function(r){
					console.log(r.message);
					frm.set_value('post_code', r.message);
					frm.set_value('country', 'Australia');
				}
			})
	}
});
