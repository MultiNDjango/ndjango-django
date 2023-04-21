/* eslint-env browser */
/* eslint
   semi: ["error", "always"],
   indent: [2, "tab"],
   no-tabs: 0,
   no-multiple-empty-lines: ["error", {"max": 2, "maxEOF": 1}],
   one-var: ["error", "always"] */
/* global REDIPS */

/* enable strict mode */
'use strict';

// create redips container
let redips = {};


// redips initialization
redips.init = function () {
	// reference to the REDIPS.drag library and message line
	let rd = REDIPS.drag,
		msg;
	// initialization
	rd.init();
	// set hover color for TD and TR
	rd.hover.colorTd = '#FFCFAE';
	rd.hover.colorTr = '#9BB3DA';
	// set hover border for current TD and TR
	rd.hover.borderTd = '2px solid #32568E';
	rd.hover.borderTr = '2px solid #32568E';
	// drop row after highlighted row (if row is dropped to other tables)
	rd.rowDropMode = 'after';
	// row was clicked - event handler
	rd.event.rowClicked = function () {
		// set current element (this is clicked TR)
		let el = rd.obj;
		// find parent table
		el = rd.findParent('TABLE', el);
		// every table has only one SPAN element to display messages
		msg = el.getElementsByTagName('span')[0];
		// display message
		msg.innerHTML = 'Clicked';
	};
	// row was moved - event handler
	rd.event.rowMoved = function () {
		// set opacity for moved row
		// rd.obj is reference of cloned row (mini table)
		rd.rowOpacity(rd.obj, 85);
		// set opacity for source row and change source row background color
		// rd.objOld is reference of source row
		rd.rowOpacity(rd.objOld, 20, 'White');
		// display message
		msg.innerHTML = 'Moved';
	};
	// row was not moved - event handler
	rd.event.rowNotMoved = function () {
		msg.innerHTML = 'Not moved';
	};
	// row was dropped - event handler
	rd.event.rowDropped = function () {
		// display message
		msg.innerHTML = 'Dropped';
	};
	// row was dropped to the source - event handler
	// mini table (cloned row) will be removed and source row should return to original state
	rd.event.rowDroppedSource = function () {
		// make source row completely visible (no opacity)
		rd.rowOpacity(rd.objOld, 100);
		// display message
		msg.innerHTML = 'Dropped to the source';
	};
	/*
	// how to cancel row drop to the table
	rd.event.rowDroppedBefore = function () {
		//
		// JS logic
		//
		// return source row to its original state
		rd.rowOpacity(rd.objOld, 100);
		// cancel row drop
		return false;
	}
	*/
	// row position was changed - event handler
	rd.event.rowChanged = function () {
		// get target and source position (method returns positions as array)
		var pos = rd.getPosition();
		// display current table and current row
		msg.innerHTML = 'Changed: ' + pos[0] + ' ' + pos[1];
	};

	// Disable dropping to already taken table cells
	REDIPS.drag.dropMode = "single"
};


// add onload event listener
if (window.addEventListener) {
	window.addEventListener('load', redips.init, false);
}
else if (window.attachEvent) {
	window.attachEvent('onload', redips.init);
}


/*
* */

// axios
// let form = document.getElementById('form'); // selecting the form
//
// form.addEventListener('submit', function(event) { // 1
//     event.preventDefault()
//
//     let data = new FormData(); // 2
//
//     data.append("title", document.getElementById('title').value)
//     data.append("note", document.getElementById('note').value)
//     data.append("csrfmiddlewaretoken", '{{csrf_token}}') // 3
//
//     axios.post('create_note/', data) // 4
//      .then(res => alert("Form Submitted")) // 5
//      .catch(errors => console.log(errors)) // 6
//
// })


function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== "") {
		const cookies = document.cookie.split(";");
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + "=")) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}


// axios.defaults.xsrfCookieName = 'csrftoken'
// axios.defaults.xsrfHeaderName = "X-CSRFToken"
// axios.defaults.headers.common['X-CSRFToken'] = getCookie("csrftoken");
// axios.defaults.withCredentials = true


// axios call
function sendAxios(url, method, data) {
	try {
		const response = axios({
			method: method,
			url: url,
			xsrfCookieName: 'csrftoken',
			xsrfHeaderName: 'X-CSRFToken',
			headers: {
				"X-Requested-With": "XMLHttpRequest",
				"X-CSRFToken": getCookie("csrftoken"),
			},
			data: data
		})
			.then(data => {
				console.log(data)
				location.reload();
			})

	} catch (error) {
		console.error(error);
	}
}



// convert input table to dict
function tableToDict(table) {
    var header = [];
    var rows = [];

    // header
    for (let i = 0; i < table.rows[0].cells.length; i++) {
        header.push(table.rows[0].cells[i].innerHTML);
    }
    // console.log(header)

    for (let i = 1; i < table.rows.length -1; i++) {
        var row = {};
        // console.log(i+"째 줄")
        for (let j = 1; j < table.rows[i].cells.length; j++) {
            // console.log(j+"째 칸")
            // console.log(table.rows[i].cells[j].innerText)
            try {
                const td = table.rows[i].cells[j]
				// const input = td.getElementsByTagName('uid').innerText
                const input = td.querySelector('small').innerText
                row[j] = input
                // console.log('row[j]: '+ j +" "+ row[j])
            } catch {
                // 빈 cell
                row[j] = null
                // console.log('row[j]: '+ row[j])
            }

        }
        rows.push(row);
        // console.log(row)

        // console.log(table.rows[i].cells[1].innerText)
        // const td = table.rows[i].cells[1]
        // const input = td.querySelector('span').innerText
    }
    // console.log(JSON.stringify(rows))

    const final = {}
    final[header[0]] = rows

    return final
}

// convert fridge(ice+fresh) tables into json
async function tableToJson(user, table, table2) {
    const ice = tableToDict(table)
    // console.log(JSON.stringify(rows))
    const fresh = tableToDict(table2)
    // console.log(JSON.stringify(rows2))
    const fridge = { ...ice, ...fresh };
	// const data = {[user]:fridge}
	// const data = { userIds : fridge}
	let data = {}
	if (user == "None") {
		// data['user'] = null
		console.log("user is not authenticated")
		return
	}
	// } else {
	// 	data['user'] = user
	// }
	data['location'] = fridge

    console.log(JSON.stringify(data))

    // axiosPost('/refrigerators/two-doors/fridge', fridge)
	// editMsg(fridge)
	const url = `/refrigerators/two-doors/${user}`
	console.log(url)
	let response = await sendAxios(url, 'patch', data)


}