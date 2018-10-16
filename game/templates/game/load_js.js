var byPosition = [], byTeam = [];


		$("input[name=position]").on( "change", function() {
			if (this.checked) byPosition.push("[data-category~='" + $(this).attr("value") + "']");
			else removeA(byPosition, "[data-category~='" + $(this).attr("value") + "']");
		});

		$("input[name=team-name]").on( "change", function() {
			if (this.checked) byTeam.push("[data-category~='" + $(this).attr("value") + "']");
			else removeA(byTeam, "[data-category~='" + $(this).attr("value") + "']");
		});


		$("input").on( "change", function() {
			var str = "Include items \n";
			var selector = '', cselector = '', nselector = '';

			var $lis = $('.players > div'),
				$checked = $('input:checked');

			if ($checked.length) {

				if (byPosition.length) {
					if (str == "Include items \n") {
						str += "    " + "with (" +  byPosition.join(',') + ")\n";
						$($('input[name=position]:checked')).each(function(index, byPosition){
							if(selector === '') {
								selector += "[data-category~='" + byPosition.id + "']";
							} else {
								selector += ",[data-category~='" + byPosition.id + "']";
							}
						});
					} else {
						str += "    AND " + "with (" +  byPosition.join(' OR ') + ")\n";
						$($('input[name=position]:checked')).each(function(index, byPosition){
							selector += "[data-category~='" + byPosition.id + "']";
						});
					}
				}

				if (byTeam.length) {
					if (str == "Include items \n") {
						str += "    " + "with (" +  byTeam.join(' OR ') + ")\n";
						$($('input[name=team-name]:checked')).each(function(index, byTeam){
							if(selector === '') {
								selector += "[data-category~='" + byTeam.id + "']";
							} else {
								selector += ",[data-category~='" + byTeam.id + "']";
							}
						});
					} else {
						str += "    AND " + "with (" +  byTeam.join(' OR ') + ")\n";
						$($('input[name=team-name]:checked')).each(function(index, byTeam){
							if(cselector === '') {
								cselector += "[data-category~='" + byTeam.id + "']";
							} else {
								cselector += ",[data-category~='" + byTeam.id + "']";
							}
						});
					}
				}

				$lis.hide();
				console.log(selector);
				console.log(cselector);

				if (cselector === '') {
					$('.flowers > div').filter(selector).show();
				} else {
					$('.flowers > div').filter(selector).filter(cselector).show();
				}

			} else {
				$lis.show();
			}

			$("#result").html(str);

		});

		function removeA(arr) {
			var what, a = arguments, L = a.length, ax;
			while (L > 1 && arr.length) {
				what = a[--L];
				while ((ax= arr.indexOf(what)) !== -1) {
					arr.splice(ax, 1);
				}
			}
			return arr;
		}
