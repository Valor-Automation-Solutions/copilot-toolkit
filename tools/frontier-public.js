/* Public conference material only. Profile values remain in this browser. */
(function(root){
  'use strict';
  /* Query-level vocabulary, never a list of hand-picked conference items. */
  var GROUPS=[
    {test:/\brpa\b|אוטומצ|power automate|workflow|זרימ|רובוט|דטרמיניסט/i,
      terms:'power automate workflow agent flows אוטומציה תהליך זרימה דטרמיניסטי תזמור',anchor:'power automate'},
    {test:/אבטח|סייבר|security|defender/i,
      terms:'אבטחה אבטחת מידע סיכון סיכונים הרשאות הזרקת פרומפט הגנה מדיניות security defender'},
    {test:/כספ|חשב|תקציב|שכר|תשלום|גבייה|רכש|finance|invoice/i,
      terms:'כספים חשבונית חשבוניות מחיר תשלום תקציב רכש עלות finance invoice'},
    {test:/שירות|לקוח|פניות|פנייה|מוקד|service|customer|support/i,
      terms:'שירות לקוחות פניות מוקד תמיכה customer support'},
    {test:/הדרכה|הכשרה|למידה|גיוס|קליטה|משאב|onboarding|training/i,
      terms:'הדרכה הכשרה למידה קליטה עובדים מרכז מצוינות training onboarding'},
    {test:/תפעול|לוגיסט|אספקה|מלאי|משלוח|operations/i,
      terms:'תפעול לוגיסטיקה אספקה מלאי משלוח תהליך operations'},
    {test:/טכנולוג|מערכות|מחשוב|טננט|developer|agent 365/i,
      terms:'מחשוב מפתח פיתוח טננט סוכנים ממשל developer agent 365'}
  ];
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
  function stem(word){return word.replace(/^וה(?=.{4})|^ה(?=.{4})/,'').replace(/(?:יים|ים|ות|ית)$/,'').replace(/s$/,'')}
  function hasTerm(value,term){var target=stem(term);return words(value).some(function(word){return word===term||stem(word)===target})}
  function queryTerms(query){
    var literal=words(query), expanded=[];
    if(literal.length>1)literal=literal.filter(function(term){return !/^(מפתח|מפתחת|נציג|נציגת|צוות|מנהל|מנהלת|עובד|עובדת)$/.test(term)});
    var group=GROUPS.find(function(candidate){return candidate.test.test(query)});
    if(group)expanded=words(group.terms);
    var required=[];
    if(/שכר|payroll/i.test(query))required=['שכר','משכורת','תלוש','payroll'];
    else if(/שירות|מוקד|פניי|פניו|support/i.test(query))required=['שירות','מוקד','פניות','פנייה','תמיכה','service','support'];
    var customerSupport=/שירות לקוחות|נציג(?:ת)? שירות|מוקד שירות|customer service/i.test(query);
    return {literal:literal,expanded:expanded.filter(function(term){return literal.indexOf(term)<0}),anchor:group&&group.anchor,required:required,customerSupport:customerSupport};
  }
  function rank(items,query,profile){
    var terms=queryTerms(query), q=normalize(query);
    return items.map(function(item){
      var title=normalize(item.title), short=normalize(item.what+' '+item.detail), body=normalize(item.text), direct=0, expanded=0;
      if(terms.customerSupport&&!/שירות לקוחות|פני(?:יה|ות) לקוחות|מוקד|תמיכה בלקוחות|customer service/i.test(title+' '+short))return {item:item,score:0,eligible:false};
      if(terms.required.length&&!terms.required.some(function(term){return hasTerm(title+' '+short,term)}))return {item:item,score:0,eligible:false};
      if(q.length>2&&title.includes(q))direct+=12;
      if(q.length>2&&short.includes(q))direct+=6;
      terms.literal.forEach(function(term){
        var base=stem(term);
        if(hasTerm(title,term)||hasTerm(title,base))direct+=8;
        if(hasTerm(short,term)||hasTerm(short,base))direct+=5;
        if(hasTerm(body,term)||hasTerm(body,base))direct+=2;
      });
      terms.expanded.forEach(function(term){
        if(hasTerm(title,term))expanded+=3;
        else if(hasTerm(short,term))expanded+=2;
      });
      if(terms.anchor&&(title.includes(terms.anchor)||short.includes(terms.anchor)))expanded+=6;
      return {item:item,score:direct+expanded,eligible:direct>=7||expanded>=5};
    }).filter(function(result){return result.eligible&&decision(result.item,profile||{}).label!=='לא רלוונטי לנו'})
      .sort(function(a,b){return b.score-a.score||a.item.id.localeCompare(b.item.id)})
      .filter(function(result,index,list){return result.score>=Math.max(4,(list[0]||{score:0}).score*0.7)})
      .slice(0,5).map(function(result){return result.item});
  }
  function decision(item,profile){
    var core=item.session+' '+item.title+' '+item.what+' '+item.detail;
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
