/* Public conference material only. Profile values remain in this browser. */
(function(root){
  'use strict';
  var GROUPS={
    finance:['כספ','חשב','תקציב','שכר','תשלום','מחיר','עלות','גבייה','רכש','חשבונית','finance','invoice'],
    service:['שירות','לקוח','פנייה','פניות','מוקד','תמיכה','תלונה','service','customer','support'],
    people:['עובד','גיוס','קליטה','הדרכה','הכשרה','למידה','משאב','מנהלת ידע','hr','onboarding','training'],
    operations:['תפעול','לוגיסט','אספקה','מלאי','משלוח','תהליך','זרימת עבודה','אוטומציה','ספק','operations','workflow'],
    technology:['טכנולוג','מערכות','אבטח','מחשוב','טננט','מפתח','בונה סוכנים','it','security','developer','agent 365']
  };
  var CAPABILITIES=[
    ['copilot','Microsoft 365 Copilot',/\b(?:microsoft 365 )?copilot\b|קופיילוט/i],
    ['power','Power Platform',/power platform|power automate|power apps/i],
    ['sharepoint','SharePoint',/sharepoint|שרפוינט/i],
    ['teams','Teams',/\bteams\b|טימס/i],
    ['studio','Copilot Studio',/copilot studio/i],
    ['azure','Azure',/\bazure\b/i],
    ['credits','Copilot Credits',/copilot credits|קרדיטים/i],
    ['e5','E5',/\be5\b/i],
    ['defender','Defender',/defender/i],
    ['entra','Entra P1',/entra p1/i],
    ['agent365','Agent 365',/agent 365/i]
  ];
  function normalize(value){return String(value||'').toLocaleLowerCase().normalize('NFKD').replace(/[\u0591-\u05c7]/g,'').replace(/[׳״'".,:;()\[\]{}!?־-]/g,' ').replace(/\s+/g,' ').trim()}
  function words(value){return normalize(value).split(/\s+/).filter(function(word){return word.length>1})}
  function stem(word){return word.replace(/^[והבלכשמ]{1,2}(?=.{3})/,'').replace(/(?:ים|ות|ית|יים|יים)$/,'')}
  function overlap(needle,haystack){return needle.some(function(term){return haystack.indexOf(term)>=0||haystack.some(function(word){return stem(word)===stem(term)})})}
  function queryTerms(query){
    var literal=words(query), expanded=[];
    Object.keys(GROUPS).forEach(function(group){if(overlap(literal,words(GROUPS[group].join(' '))))expanded=expanded.concat(words(GROUPS[group].join(' ')))});
    return {literal:literal,expanded:expanded.filter(function(term){return literal.indexOf(term)<0})};
  }
  function rank(items,query){
    var terms=queryTerms(query), q=normalize(query);
    return items.map(function(item){
      var title=normalize(item.title), short=normalize(item.what+' '+item.detail), body=normalize(item.text), direct=0, expanded=0;
      if(q.length>2&&title.includes(q))direct+=12;
      if(q.length>2&&short.includes(q))direct+=6;
      terms.literal.forEach(function(term){
        var base=stem(term);
        if(title.includes(term)||title.includes(base))direct+=8;
        if(short.includes(term)||short.includes(base))direct+=5;
        if(body.includes(term)||body.includes(base))direct+=2;
      });
      terms.expanded.forEach(function(term){
        if(title.includes(term))expanded+=2;
        else if(short.includes(term))expanded+=1;
      });
      return {item:item,score:direct+expanded,eligible:direct>=7||expanded>=5};
    }).filter(function(result){return result.eligible}).sort(function(a,b){return b.score-a.score||a.item.id.localeCompare(b.item.id)})
      .filter(function(result,index,list){return result.score>=Math.max(4,(list[0]||{score:0}).score*0.7)})
      .slice(0,5).map(function(result){return result.item});
  }
  function decision(item,profile){
    var core=item.title+' '+item.what+' '+item.detail;
    var found=CAPABILITIES.filter(function(c){return c[2].test(core)});
    var excluded=found.filter(function(c){return profile[c[0]]==='excluded'});
    var missing=found.filter(function(c){return profile[c[0]]==='no'});
    var unknown=found.filter(function(c){return !['yes','no','excluded'].includes(profile[c[0]])});
    var early=/frontier|preview|גישה מוקדמת|פריוויו|טרם שוחרר|לא זמין/i.test(item.text);
    if(excluded.length){
      return {label:'לא רלוונטי לנו',reason:'הפרופיל המקומי מסמן כלא בתכנון: '+excluded.map(function(c){return c[1]}).join(', ')+'.'};
    }
    if(missing.length){
      return {label:'דורש תקציב או אישור',reason:'סומנו כחסרים: '+missing.map(function(c){return c[1]}).join(', ')+'. יש לאמת במקור את דרישת הרישוי המדויקת.'};
    }
    if(unknown.length||early){
      return {label:'דורש תקציב או אישור',reason:(unknown.length?'יש לבדוק זמינות וזכאות ל־'+unknown.map(function(c){return c[1]}).join(', ')+'. ':'')+(early?'המקור מתאר גישה מוקדמת או זמינות שטרם הוכחה.':'')};
    }
    if(found.length){return {label:'אפשר להפעיל היום',reason:'היכולות שזוהו במקור סומנו כזמינות בפרופיל המקומי. יש לאמת תנאי רישוי לפני הפעלה.'}}
    if(/דפוס|מסגרת|הכשרה|הדרכה|מדידה|שאלות|תהליך|מרכז מצוינות/i.test(core)){
      return {label:'אפשר להפעיל היום',reason:'זהו דפוס עבודה או דיון שאפשר להתחיל לבחון בלי שנמצאה במקור דרישת מוצר נוספת.'};
    }
    return {label:'דורש תקציב או אישור',reason:'המקור אינו מוכיח שאפשר להפעיל את הדוגמה עם הרישוי שהוזן; בדקו זמינות ועלות.'};
  }
  root.FrontierPublic={rank:rank,decision:decision,capabilities:CAPABILITIES};
  if(typeof module!=='undefined'&&module.exports)module.exports=root.FrontierPublic;
})(typeof window!=='undefined'?window:globalThis);
