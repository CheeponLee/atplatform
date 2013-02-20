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
	$(".bottomtooltip").tooltip({placement:'bottom',delay:{ show: 100, hide: 800 }});
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
        var index = getdomobject('td','',{'name':j,'width':20});
        tr.appendChild(index);
        var indexvalue = getdomobject('a',j,{});
        index.appendChild(indexvalue);
        indexvalue.href='/passreport/www/'+planname+'/planinfo.html#'+String(j);
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
    var index = getdomobject('td','',{'name':j,'width':20});
	tr.appendChild(index);
    var indexvalue = getdomobject('a',j,{});
    index.appendChild(indexvalue);
    indexvalue.href='/passreport/www/'+planname+'/casesexcuteinfo.html#'+String(j);
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

//customdata_load
function customdata_loaddata()
{
    var casedata_location=document.getElementById('casedata_location');
    for (var casename in cases)
    {
        var utildata = cases[casename][6];
        var p_a=false;
        for (var datatype in utildata)
        {
            p_a=true;break;
        }
        if (p_a==true)
        {
            var casedom=document.createElement('div');
            casedom.setAttribute('class','row thumbnaillike');
            casedom.setAttribute('id',casename);
            casedata_location.appendChild(casedom);
            //the title
            var titledom=document.createElement('h4');
            titledom.innerHTML=casename;
            casedom.appendChild(titledom);
            casedom.appendChild(document.createElement('hr'));
            //set pics
            if (utildata.hasOwnProperty('pic'))
            {
                var pichead=document.createElement('div');
                pichead.setAttribute('class','row')
                casedom.appendChild(pichead);
                var pichead_p=document.createElement('p');
                pichead_p.setAttribute('class','span2');
                var pichead_b=document.createElement('b');
                pichead_b.innerHTML='图片';
                pichead.appendChild(pichead_p);
                pichead_p.appendChild(pichead_b);
                //pic body
                var picbody=document.createElement('div');
                picbody.setAttribute('class','row');
                picbody.setAttribute('id',casename+'_pic');
                casedom.appendChild(picbody);
                var picbodyvalue=document.createElement('div');
                picbody.appendChild(picbodyvalue);
                picbodyvalue.setAttribute('class','span12');
                //set pic body value
                var thumbnails=document.createElement('ul');
                thumbnails.setAttribute('class','thumbnails');
                picbodyvalue.appendChild(thumbnails);
                for (var data in utildata['pic'])
                {
                    var picname=utildata['pic'][data];
                    var li=document.createElement('li');
                    var a=document.createElement('a');
                    var img=document.createElement('img');
                    thumbnails.appendChild(li);
                    li.appendChild(a);
                    a.appendChild(img);
                    li.setAttribute('class','span3');
                    a.setAttribute('href','/static/resfiles/'+String(planname)+'/'+String(casename)+'/'+String(picname));
                    a.setAttribute('rel','lightbox['+String(casename)+']');
                    a.setAttribute('title',casename);
                    a.setAttribute('class','thumbnail');
                    img.setAttribute('src','/static/resfiles/'+String(planname)+'/'+String(casename)+'/'+String(picname));
                }
            }
            //set texts
            if (utildata.hasOwnProperty('text'))
            {
                var texthead=document.createElement('div');
                texthead.setAttribute('class','row')
                casedom.appendChild(texthead);
                var texthead_p=document.createElement('p');
                texthead_p.setAttribute('class','span2');
                var texthead_b=document.createElement('b');
                texthead_b.innerHTML='文本';
                texthead.appendChild(texthead_p);
                texthead_p.appendChild(texthead_b);
                //pic body
                var textbody=document.createElement('div');
                textbody.setAttribute('class','row');
                textbody.setAttribute('id',casename+'_text');
                casedom.appendChild(textbody);
                var textbodyvalue=document.createElement('div');
                textbody.appendChild(textbodyvalue);
                textbodyvalue.setAttribute('class','span12');
                //set pic body value
                var thumbnails=document.createElement('ul');
                thumbnails.setAttribute('class','thumbnails');
                textbodyvalue.appendChild(thumbnails);
                for (var data in utildata['text'])
                {
                    var text=utildata['text'][data];
                    var li=document.createElement('li');
                    var a=document.createElement('a');
                    thumbnails.appendChild(li);
                    li.appendChild(a);
                    li.setAttribute('class','span3 hidetext');
                    a.setAttribute('href','javascript:void(0)');
                    a.innerHTML=text;
                    if (li.clientWidth<li.scrollWidth)
                    {
                        li.setAttribute('class', li.getAttribute('class')+' bottomtooltip');
                        li.setAttribute('title',text);
                    }
                }
            }
            //set files
            if (utildata.hasOwnProperty('file'))
            {
                var filehead=document.createElement('div');
                filehead.setAttribute('class','row')
                casedom.appendChild(filehead);
                var filehead_p=document.createElement('p');
                filehead_p.setAttribute('class','span2');
                var filehead_b=document.createElement('b');
                filehead_b.innerHTML='文件';
                filehead.appendChild(filehead_p);
                filehead_p.appendChild(filehead_b);
                //pic body
                var filebody=document.createElement('div');
                filebody.setAttribute('class','row');
                filebody.setAttribute('id',casename+'_text');
                casedom.appendChild(filebody);
                var filebodyvalue=document.createElement('div');
                filebody.appendChild(filebodyvalue);
                filebodyvalue.setAttribute('class','span12');
                //set pic body value
                var thumbnails=document.createElement('ul');
                thumbnails.setAttribute('class','thumbnails');
                filebodyvalue.appendChild(thumbnails);
                for (var data in utildata['file'])
                {
                    var filename=utildata['file'][data];
                    var li=document.createElement('li');
                    var a=document.createElement('a');
                    var i=document.createElement('i');
                    thumbnails.appendChild(li);
                    li.appendChild(a);
                    li.setAttribute('class','span3 hidetext');
                    a.setAttribute('href','/static/resfiles/'+String(planname)+'/'+String(casename)+'/'+String(filename));
                    a.setAttribute('class','thumbnaillike');
                    a.appendChild(i)
                    i.setAttribute('class','icon-file');
                    var filenamenode=document.createTextNode(filename);
                    a.appendChild(filenamenode);
                    if (li.clientWidth<li.scrollWidth)
                    {
                        li.setAttribute('class', li.getAttribute('class')+' bottomtooltip');
                        li.setAttribute('title',filename);
                    }
                }
            }
            loadtooltip();
            casedom.appendChild(document.createElement('br'));
        }
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