/*
	cambiar impresora 
	document.querySelector("print-preview-app").__data.destination_.id_ = "Adobe PDF"
*/

	let qcode = document.querySelector("#qcode");
	let serie_factura = document.querySelector("#serie");
	let no_factura = document.querySelector("#no_factura");
	let fecha = document.querySelector("#fecha");
	let nit = document.querySelector("#nit");
	let nombre = document.querySelector("#nombre");
	let codigo = document.querySelector("#codigo");
	let monto = document.querySelector("#monto");
	let fecha_pago = document.querySelector("#fecha_pago");
	let empresa = document.querySelector("#empresa");

	no_factura.focus();

	no_factura.addEventListener('keydown', function(e){
		if(e.keyCode === 46 || e.keyCode === 8){
			clean();
		}
		else if (e.keyCode === 13 || e.keyCode === 9 ){
			buscar_factura(no_factura.value);
		}

	});

function clean() {
	qcode.src = "data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=";
	empresa.value ="";
	serie_factura.value ="";
	nit.value = "";
	nombre.value ="";
	codigo.value ="";
	monto.value="";
	fecha_pago.value="";

}
let toCurrency = (valor)=>{
	valor = parseFloat(valor);
	return (valor).toLocaleString('es-GT', {
		style: 'currency',
		currency: 'GTQ',
	});
}

monto.addEventListener('input', e =>{

});

	const formatRegional = (valor) =>{
	    const expr = /(\d)(?=(\d{3})+(?!\d))/g;
	    const rep = '$1,';
	    return valor.toString().replace(expr, rep);
	}



function openWin()
  {
	if (no_factura.value !== ""  &&  qcode.src !== ""){
		PrintDialog=window.open('Imprimir','test imprimir','width=(screen.width/2)-(w/2),height=(screen.height/2)-(h/2)');
		PrintDialog.document.write("<div style='text-align: center; font-family: sans-serif; font-size: 12;'>");
		PrintDialog.document.write("<p style='text-align=center;'><img width=96 height=96 src='"+qcode.src+"''>");
		PrintDialog.document.write("<h2><b>"+document.querySelector("#title").innerText+"</h2>")
		PrintDialog.document.write("<p><b>"+empresa.value+"</b></p>")
		PrintDialog.document.write("<hr style='border-style: dashed;'>")
		PrintDialog.document.write("<p><b>Fecha Factura:</b> "+fecha.value+"</p>");
		PrintDialog.document.write("<p><b>Factura:</b> "+serie_factura.value+"-"+no_factura.value+"</p></p>");
		PrintDialog.document.write("<p><b>Nombre:</b> "+nombre.value+"</p>");
		PrintDialog.document.write("<p><b>Pago:</b> "+new Date(fecha_pago.value).toLocaleString()+"</p>");
		PrintDialog.document.write("<p><b>Monto:</b> "+monto.value+"</p>");
		PrintDialog.document.write("<br><br><br>");
		PrintDialog.document.write("<p>"+new Date().toLocaleString()+"</p>");
		PrintDialog.document.write("</div>");
		PrintDialog.document.write('<script>document.querySelector("print-preview-app").__data.destination_.id_ = "Adobe PDF"</script>')
		// PrintDialog.document.close();
		// PrintDialog.focus();
		PrintDialog.print(); //DOES NOT WORK 
		}
	else {
		alert("Ingrese primero un Numero de Factura");
		no_factura.focus();
	}
  }


var obj = new Object();
const buscar_factura = (valor) =>{
	fetch(window.origin+"/api/v1/facturas_pagos?nofac="+valor).then(function(response) {
		if(response.ok) {
			response.json().then(
				data => {
					obj = data;
					if ( !(data['invoice'].length === 0) ) {
						for (let index in data) {
							serie_factura.value = data["invoice"][0].serie;
							fecha.valueAsDate = new Date(data["invoice"][0].fecha);
							nit.value = data["invoice"][0].nit;
							nombre.value = decodeURI(data["invoice"][0].nombre);
							codigo.value = data["invoice"][0].qsys_codigo_cliente;
							monto.value = toCurrency(data["invoice"][0].monto); 
							fecha_pago.valueAsNumber  = new Date(data["invoice"][0].fecha_pago).getTime() -  new Date('1970/01/01').getTime(); //-21600000
							qcode.src = 'data:img/png;base64,'+data['qcode'];
							empresa.value = data["invoice"][0].empresa
						}
					}
					else if (data['invoice'].length === 0){
						Swal.fire({
							icon: 'info',
							title: 'No encontramos nada para mostrar...',
							confirmButtonColor: '#3085d6',
							text: 'Oops...! \uD83D\uDE14',
							footer: '<b>El numero de Factura puede que no Aplique para esta opcion</b>'
						});
					}
				});

		} else {
			console.log('Respuesta de red OK pero respuesta HTTP no OK');
		}
		}).catch(function(error) {
			console.log('Hubo un problema con la petición Fetch:' + error.message);
	});

}





// var el = document.querySelector("#input");

	// el.addEventListener('keypress', function(e){ 
	// 	var val;
	// 	val = el.value.replaceAll(',', '');
	// 	el.value = formatRegional(val);
	// 	console.log(el.value);
 //   	});

	// const formatRegional = (valor) =>{
	//     const expr = /(\d)(?=(\d{3})+(?!\d))/g;
	//     const rep = '$1,';
	//     return valor.toString().replace(expr, rep);
	// }
