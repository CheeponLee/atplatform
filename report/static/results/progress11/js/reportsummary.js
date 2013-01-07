// Global Var
var currentclickedli='reportsummary';

//timedataformat
function Appendzero(obj)
{
 if(obj<10) return "0" +""+ obj;
 else return obj;
     
}
function date2str(x,y) {
    var z = {
        y: x.getFullYear(),
        M: x.getMonth()+1,
        d: x.getDate(),
        h: Appendzero(x.getHours()),
        m: Appendzero(x.getMinutes()),
        s: Appendzero(x.getSeconds())
    };
    return y.replace(/(y+|M+|d+|h+|m+|s+)/g,function(v) {
        return ((v.length>1?"0":"")+eval('z.'+v.slice(-1))).slice(-(v.length>2?v.length:2))
    });
}
function getformattime(timenum)
{
	return date2str(new Date(timenum*1000), "yyyy-M-d h:m:s" )
	}

//chart
function basic_pie(container) {

  var
    d1 = [[0, sumofpassedcases]],
    d2 = [[0, sumofcases-sumofpassedcases]],
    graph;
  
  graph = Flotr.draw(container, [
    { data : d1, label : 'success' },
    { data : d2, label : 'failed',
      pie : {
        explode : 8
      }
    }
  ], {
	  colors: ['#0066FF', '#FF0000', '#33CC00', '#33CC00', '#33CC00'],
    HtmlText : false,
    grid : {
      verticalLines : false,
      horizontalLines : false
    },
	title :'执行成功率'
	,
    xaxis : { showLabels : false },
    yaxis : { showLabels : false },
    pie : {
      show : true, 
      explode : 6
    },
    mouse : { track : true },
    legend : {
      position : 'se',
      backgroundColor : '//D2E8FF'
    }
  });
}
function showchart(){
basic_pie(document.getElementById("summarycontainer"));
}

//tooltip
function loadtooltip(){
	$(".lefttooltip").tooltip({placement:'left',delay:{ show: 100, hide: 1500 }});
	$(".toptooltip").tooltip({placement:'top',delay:{ show: 100, hide: 800 }});
	$(".righttooltip").tooltip({placement:'right',delay:{ show: 100, hide: 800 }});
	$(".bottom").tooltip({placement:'bottom',delay:{ show: 100, hide: 800 }});
}


//getsumcases
function getsumofpassedcases()
{
	sum=0;
	for (i in cases)
	{
		if (cases[i][3]=="success")
		{
			sum+=1;
			}
		}
	return sum;
	}

//getdomobject
function getdomobject(nodetag,value,attributes){
	node = document.createElement(nodetag);
	node.innerHTML=value;
	for (attr in attributes)
	{
		node.setAttribute(attr,attributes[attr]);
		}
	return node;
	}

//appendcasetoelement
function appendcaseinfo(element){
	var j=1;
	for (_case in cases)
	{
	var tr = document.createElement("tr");
	casename=_case;
	starttime=getformattime(cases[_case][1]);
	endtime=getformattime(cases[_case][2]);
	durtime=(cases[_case][2]-cases[_case][1]).toFixed(2);
	stopstatus=cases[_case][0];
	issuccess=cases[_case][3];
	if (issuccess=="success")
	{
		tr.setAttribute('class','success');
		}
	else
	{
		tr.setAttribute('class','error');
		}
	errormsg=cases[_case][4];
	var errormsgdom=document.createElement("td");
	if (errormsg!="")
	{
		var errormsgdoma=document.createElement("a");
		errormsgdoma.setAttribute("class","lefttooltip");
		errormsgdoma.setAttribute("title",errormsg);
		errormsgdoma.innerHTML=errormsg;
		errormsgdom.appendChild(errormsgdoma);
	}
	errorpic=cases[_case][5];
	var errorpicdom=document.createElement("td");;
	if (errorpic!="")
	{
		var errorpicdoma=document.createElement("a");
		errorpicdoma.setAttribute("href","/exceptionpic/"+errorpic);
		errorpicdoma.setAttribute("rel","lightbox");
		errorpicdoma.setAttribute("title",errormsg);
		errorpicdom.appendChild(errorpicdoma);
		var errorpicdomimg=document.createElement("img");
		errorpicdomimg.src="/exceptionpic/"+errorpic;
		errorpicdomimg.setAttribute("style","height:100px");
		errorpicdoma.appendChild(errorpicdomimg);
		}
	tr.appendChild(getdomobject('td',j,{'name':j,'width':20}));
	var casenamedom=getdomobject('td',_case,{'class':'toptooltip','title':_case});
	var starttimedom=getdomobject('td',starttime,{});
	var endtimedom=getdomobject('td',endtime,{});
	var durtimedom=getdomobject('td',durtime,{});
	var stopstatusdom=getdomobject('td',stopstatus,{});
	var issuccessdom=getdomobject('td',issuccess,{});
	tr.appendChild(casenamedom);	tr.appendChild(starttimedom);	tr.appendChild(endtimedom);	tr.appendChild(durtimedom);
		tr.appendChild(stopstatusdom);	tr.appendChild(issuccessdom);	tr.appendChild(errormsgdom);	tr.appendChild(errorpicdom);
	element.appendChild(tr);
	for (var e=0;e<7;e=e+1)
	{
		var t=tr.childNodes[e];
		if (t.clientWidth<t.scrollWidth)
		{
			t.setAttribute('class','toptooltip');
			t.setAttribute('title',t.innerHTML);
		}
		else
		{t.setAttribute('class','orgtd');}
	} 
	j=j+1;
	}
}

//appendplancaseinfo
function appendplancaseinfo(element){
	var j=1;
	for (i in plancases)
	{
	var tr = document.createElement("tr");
	tr.appendChild(getdomobject('td',j,{'name':j,'width':20}));
	var casename=getdomobject('td',plancases[i][0],{});
	var Browsername=getdomobject('td',plancases[i][1]['Browsername'],{});
	var Browserversion=getdomobject('td',plancases[i][1]['Browserversion'],{});
	var Platform=getdomobject('td',plancases[i][1]['Platform'],{});
	var Javascriptenabled=getdomobject('td',plancases[i][1]['Javascriptenabled'],{});
	tr.appendChild(casename);
	tr.appendChild(Browsername);
	tr.appendChild(Browserversion);
	tr.appendChild(Platform);
	tr.appendChild(Javascriptenabled);
	element.appendChild(tr);
	for (var e=0;e<6;e=e+1)
	{
		var t=tr.childNodes[e];
		if (t.clientWidth<t.scrollWidth)
		{
			if (e!=5)
			{
				t.setAttribute('class','toptooltip');
			}
			else
			{
				t.setAttribute('class','lefttooltip');
			}
			t.setAttribute('title',t.innerHTML);
		}
		else
		{t.setAttribute('class','orgtd');}
	} 
	j=j+1;
	}
}

//changecss
function changecss(e){
	var predom=document.getElementById(currentclickedli);
	predom.removeAttribute('class');
	this.setAttribute('class','active')
	currentclickedli=this.getAttribute('id')
	}

//filldatatoelement
function filldata(id,value){
	title=value;
	innerhtml=document.getElementById(id).innerHTML;
	document.getElementById(id).innerHTML=innerhtml+value;
	}

//pageloads

function frontpage_load()
{
	var left=document.getElementById('left')
	for (i=1;i<left.childElementCount;i++)
	{
		left.children[i].addEventListener('click',changecss,true)
	}
}


function summary_loaddata(){
	sumofpassedcases=getsumofpassedcases();
	filldata("planedtime",getformattime(planedtime));
	filldata("planstarttime",getformattime(planstarttime));
	filldata("planendtime",getformattime(planendtime));
	filldata("sumofexcutetime",(planendtime-planstarttime).toFixed(2)+"秒");
	filldata("sumofcases",sumofcases);
	filldata("sumofpassedcases",sumofpassedcases);
	filldata("sumoffailedcases",sumofcases-sumofpassedcases);
	filldata("passpercent",((sumofpassedcases/sumofcases)*100).toFixed(2)+"%");
	showchart();
}

function casesexcuteinfo_loaddata(){
	sumofpassedcases=getsumofpassedcases();
	filldata("sumofcases",sumofcases);
	filldata("sumofpassedcases",sumofpassedcases);
	filldata("sumoffailedcases",sumofcases-sumofpassedcases);
	filldata("passpercent",((sumofpassedcases/sumofcases)*100).toFixed(2)+"%");
	appendcaseinfo(document.getElementById("caseinfobody"));
	loadtooltip();
}

function planinfo_loaddata(){
	filldata("planname",planname);
	filldata("sumofcases",plancases.length);
	filldata("planedtime",getformattime(planedtime));
	filldata("planstarttime",getformattime(planstarttime));
	filldata("planendtime",getformattime(planendtime));
	filldata("sumofexcutetime",(planendtime-planstarttime).toFixed(2)+"秒");
	
	appendplancaseinfo(document.getElementById("planinfobody"));
	loadtooltip();
	}