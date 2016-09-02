"use strict";



function showUserFavData(evt) {
  var favorites = [];
  var favs = $('.favs');
  console.log(favs)
  /*for fav in favs*/
  for (var fav=0; fav< favs.length; fav++){
    favorites.push(fav.data('fav'));
} var info = {'favs': favorites};
$.get("/userfav.json", info, function (results) {
        console.log(results);
    });
}

 $(document).ready(showUserFavData);



/*
  var url = "/userfav.json?fav=" + fav;
  $.get(url, function (results) {
        console.log(results);
    });
}

$(document).ready(showUserFavData);*/

/*  for fav in favs* list.push/
var favs = $('.favs').data('fav');





/*create empty list []*/

/*select that div , try in JS console once it wrks then put it here, expect a list of divs, console.log everything**/


/**Ajax request goes thru the route and console.log (result)
in the for loop */


/*finally modify ajax to constructs the charts in html */


