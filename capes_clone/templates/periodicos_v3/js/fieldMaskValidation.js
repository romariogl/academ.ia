/*****************************************************
*				
*				-  FIELDMASKVALIDATION.JS  -
*
*	@ DESCRIÇÃO
*		Conjunto de funções para validar dados de campos de formulário do tipo:
*
*			- Data (dd/mm/aaaa);
*				Chamada: onblur="fieldMaskValidator.data(this)";
*
*			- Hora (hh:mm);
*				Chamada: onblur="fieldMaskValidator.hora(this)";
*
*			- CPF (999.999.999-99);
*				Chamada: onblur="fieldMaskValidator.cpf(this)";
*
*			- CNPJ (99.999.999/0001-99);
*				Chamada: onblur="fieldMaskValidator.cnpj(this)";
*
*			- CEP (99999-99);
*				Chamada: onblur="fieldMaskValidator.cep(this)";
*
*			- E-mail;
*				Chamada: onblur="fieldMaskValidator.email(this)";
*
*			- Telefone sem DDD ('999-9999' ou '9999-9999');
*				Chamada: onblur="fieldMaskValidator.telefone(this)";
*
*			- Telefone com DDD ('(99) 999-9999' ou '(99) 9999-9999');
*				Chamada: onblur="fieldMaskValidator.telefoneComDDD(this)";
*
*			- Campo para somente númericos;
*				Chamada: onblur="fieldMaskValidator.soNumeros(this)";
*
*	@ AUTOR:
*		- Fábio Hemkemaier (fabiohhfarias@yahoo.com.br)
*
*****************************************************/

var fieldMaskValidator = {
	/* GLOBALS */
	_versao: '1.0',
	_dataVersao: '06/2008', // mês/ano

	/* DATA (dd/mm/aaaa) */
	data: function(field, showDiv){
		if(field.value.length > 0){
			var dataMask = /\d{2}\/\d{2}\/\d{4}/;
			if((field.value.length < 10) || (!dataMask.test(field.value))){
				//alert('A data deverá obedecer o formato: DD/MM/AAAA!');
				document.getElementById(showDiv).style.display = 'block';
				field.value = '';
				field.focus();
				this.focaCampo(field);
				return false;
			}
			else{
//				_dia = parseInt(field.value.substr(0,2));
				_dia = field.value.substr(0,2);
				_mes = field.value.substr(3,2);
				_ano = parseInt(field.value.substr(6,4));
				
				_mes30 = '04,06,09,11';
				_mes31 = '01,03,05,07,08,10,12';
				
				//valida o dia em mêses de 30 dias
				if((_mes30.indexOf(_mes) != -1) && (_dia < 1 || _dia > 30)){
					//alert('O dia deverá estar entre 01 e 30!');
					document.getElementById(showDiv).style.display = 'block';
					field.value = '';
					field.focus();
					this.focaCampo(field);
					return false;
				}
				//valida o dia em mêses de 31 dias
				if((_mes31.indexOf(_mes) != -1) && (_dia < 1 || _dia > 31)){
//					alert('Dia:'+_dia);
					//alert('O dia deverá estar entre 01 e 31!');
					document.getElementById(showDiv).style.display = 'block';
					field.value = '';
					field.focus();
					this.focaCampo(field);
					return false;
				}
				//valida o dia para o mês de fevereiro
				if(_mes == '02'){
					//bisexto
					if(_ano%4 == 0){
						if(_dia < 1 || _dia > 29){
							//alert('O dia deverá estar entre 01 e 29!');
							document.getElementById(showDiv).style.display = 'block';
							field.value = '';
							field.focus();
							this.focaCampo(field);
							return false;
						}
					}
					else{
						//normal
						if(_dia < 1 || _dia > 28){
							//alert('O dia deverá estar entre 01 e 28!');
							document.getElementById(showDiv).style.display = 'block';
							field.value = '';
							field.focus();
							this.focaCampo(field);
							return false;
						}
					}
				}
				
				//valida o mês
				if((_mes < 1) || (_mes > 12)){
					//alert('O mês deverá estar entre 01 e 12!');
					document.getElementById(showDiv).style.display = 'block';
					field.value = '';
					field.focus();
					this.focaCampo(field);
					return false;
				}
			}
		}
		
		document.getElementById(showDiv).style.display = 'none';
		return true;
	},
	
	/* HORA (hh:mm) */
	hora: function(field){
		if(field.value.length > 0){
			var horaMask = /\d{2}:\d{2}/;
			if((field.value.length < 5) || (!horaMask.test(field.value))){
				alert('A hora deverá obedecer o formato: HH:MM!');
				this.focaCampo(field);
				return false;
			}
			else{
				_hora = field.value.substr(0,2);
				_minuto = field.value.substr(3,2);
				
				//valida a hora
				if((_hora < 0) || (_hora > 23)){
					alert('A hora deverá estar entre 00 e 23!');
					this.focaCampo(field);
					return false;
				}
				//valida o minuto
				if((_minuto < 0) || (_minuto > 59)){
					alert('O minuto deverá estar entre 00 e 59!');
					this.focaCampo(field);
					return false;
				}
			}
		}
		
		return true;
	},
	
	/* CPF (999.999.999-99) */
	cpf: function(field, showDiv){
		var cpfValido = true;
		if(field.value.length > 0){
			var p_cpf = field.value.replace(/\D/g,'');
			
			if(p_cpf.length < 11)
				cpfValido = false;
			
			for(i = 0; i <= 9; i++){
				var strTemp = '';
				for(j = 0; j < 11; j++)
					strTemp += i;

				if(p_cpf == strTemp)
					cpfValido = false;
			}
			
			rcpf1 = p_cpf.substr(0,9);
			rcpf2 = p_cpf.substr(9,2);
			d1 = 0;
			for(i = 0; i < 9; i++) 
				d1 += rcpf1.charAt(i)*(10-i); 
			
			d1 = 11 - (d1 % 11); 
			if(d1 > 9)
				d1 = 0; 
			
			if(rcpf2.charAt(0) != d1) 
				cpfValido = false;
			
			d1 *= 2;
			for(i = 0; i < 9; i++)
				d1 += rcpf1.charAt(i)*(11-i); 
				
			d1 = 11 - (d1 % 11); 
			if(d1 > 9)
				d1 = 0; 
			
			if(rcpf2.charAt(1) != d1) 
				cpfValido = false;
			
			if(!cpfValido){
				document.getElementById(showDiv).style.display = 'block';
				field.value = '';
				field.focus();
				//this.focaCampo(field);
				return false;
			}
		}
		
		document.getElementById(showDiv).style.display = 'none';
		return true;
	},
	
	/* CNPJ (99.999.999/9999-99) */
	cnpj: function(field){
		var cnpjValido = true;
		if(field.value.length > 0){
			var p_cnpj = field.value.replace(/\D/g,'');
			
			if(p_cnpj.length < 14)
				cnpjValido = false;
			
			var c = p_cnpj.substr(0,12);
			var dv = p_cnpj.substr(12,2);
			var d1 = 0;
			
			for(i = 0; i < 12; i++)
				d1 += c.charAt(11-i)*(2+(i % 8));
			
			if(d1 == 0)
				cnpjValido = false;
			
			d1 = 11 - (d1 % 11);
			
			if(d1 > 9)
				d1 = 0;
			
			if(dv.charAt(0) != d1)
				cnpjValido = false;
			
			d1 *= 2;
			for(i = 0; i < 12; i++)
				d1 += c.charAt(11-i)*(2+((i+1) % 8));
			
			d1 = 11 - (d1 % 11);
			
			if(d1 > 9)
				d1 = 0;
			
			if(dv.charAt(1) != d1)
				cnpjValido = false;
			
			if(!cnpjValido){
				alert('CNPJ inválido!');
				this.focaCampo(field);
				return false;
			}
		}
		
		return true;
	},
	
	/* CEP (99999-999) */
	cep: function(field){
		if(field.value.length > 0){
			var cepMask = /\d{5}-\d{3}/;
			if(!cepMask.test(field.value)){
				alert('O CEP deverá obedecer o formato: 99999-999!');
				this.focaCampo(field);
				return false;
			}
		}
		
		return true;
	},
	
	/* TELEFONE ('999-9999' ou '9999-9999') */
	telefone: function(field){
		if(field.value.length > 0){
			var telefoneMask = /\d{3,4}-\d{4}/;
			if(!telefoneMask.test(field.value)){
				alert('O telefone deverá obedecer um dos formatos: "999-9999" ou "9999-9999"!');
				this.focaCampo(field);
				return false;
			}
		}
		
		return true;
	},
	
	/* TELEFONE COM DDD ('(99) 999-9999' ou '(99) 9999-9999') */
	telefoneComDDD: function(field){
		if(field.value.length > 0){
			var telefoneComDDDMask = /\(\d{2}\)\s\d{3,4}-\d{4}/;
			if(!telefoneComDDDMask.test(field.value)){
				alert('O telefone deverá obedecer um dos formatos: "(99) 999-9999" ou "(99) 9999-9999"!');
				this.focaCampo(field);
				return false;
			}
		}
		
		return true;
	},
	
	/* VALIDA SE CONTIVER SOMENTE NÚMEROS */
	soNumeros: function(field){
		var contemSoNumeros = true;
		var reg = /\d{1}/;
		for(i = 0; i < field.value.length; i++){
			if(!reg.test(field.value.charAt(i))){
				contemSoNumeros = false;
				break;
			}
		}
		
		if(!contemSoNumeros){
			alert('O campo deverá conter somente números!');
			this.focaCampo(field);
			return false;
		}
		else
			return true;
	},
	
	/* E-MAIL */
	email: function(field, showDiv){
		if(field.value.length > 0){
			var emailStr = field.value;
			var emailPat=/^(.+)@(.+)$/
			var specialChars="\\(\\)<>@,;:\\\\\\\"\\.\\[\\]"
			var validChars="\[^\\s" + specialChars + "\]"
			var quotedUser="(\"[^\"]*\")"
			var ipDomainPat=/^\[(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\]$/
			var atom=validChars + '+'
			var word="(" + atom + "|" + quotedUser + ")"
			var userPat=new RegExp("^" + word + "(\\." + word + ")*$")
			var domainPat=new RegExp("^" + atom + "(\\." + atom +")*$")
			var matchArray=emailStr.match(emailPat)
		
			if(matchArray==null) {
				//alert("Formato do e-mail incorreto!")
				document.getElementById(showDiv).style.display = 'block';
				field.value = '';
				this.focaCampo(field);
				return false;
			}
			var user=matchArray[1]
			var domain=matchArray[2]
		
			if (user.match(userPat)==null) {
		       	//alert("Formato do e-mail incorreto!")
		       	document.getElementById(showDiv).style.display = 'block';
				field.value = '';
				this.focaCampo(field);
				return false;
			}
		
			var IPArray=domain.match(ipDomainPat)
			if (IPArray!=null) {
		      for (var i=1;i<=4;i++) {
			    if (IPArray[i]>255) {
					    //alert("Formato do e-mail incorreto!")
					    document.getElementById(showDiv).style.display = 'block';
						field.value = '';
						this.focaCampo(field);
						return false;
				    }
			    }
		    	return true
			}
		
			var domainArray=domain.match(domainPat)
			if (domainArray==null) {
				//alert("Formato do e-mail incorreto!")
				document.getElementById(showDiv).style.display = 'block';
				field.value = '';
				this.focaCampo(field);
				return false;
			}
		
			var atomPat=new RegExp(atom,"g")
			var domArr=domain.match(atomPat)
			var len=domArr.length
			if (domArr[domArr.length-1].length<2 || 
		    	domArr[domArr.length-1].length>4) {
			    //alert("Formato do e-mail incorreto!")
			    document.getElementById(showDiv).style.display = 'block';
				field.value = '';
				this.focaCampo(field);
				return false;
			}
			
			if (len<2) {
			   var errStr="Formato do e-mail incorreto!"
			   //alert(errStr)
			   document.getElementById(showDiv).style.display = 'block';
			   field.value = '';
			   this.focaCampo(field);
			   return false;
			}
		}
		
		document.getElementById(showDiv).style.display = 'none';
		return true;
	},
	
	/* Foca e seleciona o valor do campo. */
	focaCampo: function(field){
		field.focus();
		field.select();
	}

}