function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function listBuildings() {
    alert("DEP\t\t\tDeprem Mühendisliği ve Afet Yönetimi Enstitü Binası (Ayazağa)\n\nBEB\t\t\tBilişim Enstitüsü Binası (Ayazağa)\n\nDIB\t\t\tYabancı Diller Yüksekokulu Binası (Maçka)\n\nDMB\t\t\tDenizcilik Meslek Yüksekokulu Binası (Ayazağa)\n\nDZB\t\t\tDenizcilik Binası (Tuzla)\n\nEEB\t\t\tElektrik-Elektronik Binası (Ayazağa)\n\nFEB\t\t\tFen-Edebiyat Binası (Ayazağa)\n\nGDB\t\t\tGemi İnşaatı ve Deniz Bilimleri Binası (Ayazağa)\n\nHVZ\t\t\tOlimpik Havuz (Ayazağa)\n\nINB\t\t\tİnşaat Binası (Ayazağa)\n\nISB\t\t\tİşletme Binası (Maçka)\n\nKSB\t\t\tKültür ve Sanat Birliği (Ayazağa)\n\nKMB\t\t\tKimya-Metalürji Binası (Ayazağa)\n\nKORT\t\t\tTenis Kortları (Ayazağa)\n\nMED\t\t\tMerkezi Derslik Binası (Ayazağa)\n\nMEDB\t\t\tGölet Derslik Binası(Ayazağa)\n\nMDB\t\t\tMaden Binası (Ayazağa)\n\nMIAB\t\t\tMüzik İleri Araştırmalar Merkezi (Maçka)\n\nMKB\t\t\tMakina Binası (Gümüşsuyu)\n\nMMB\t\t\tMimarlık Binası (Taşkışla)\n\nMOB\t\t\tMotorlar Binası (Ayazağa)\n\nPYB\t\t\tProje Yönetim Merkezi (Ayazağa)\n\nRSLN-M\t\t\tRuhi Sarıalp Seminer Salonu-Beden Eğitimi Bölümü(Ayazağa)\n\nSLN-M\t\t\tSpor Salonu-Beden Eğitimi Bölümü(Ayazağa)\n\nSLN-G\t\t\tSpor Salonu (Gümüşsuyu)\n\nSDKM\t\t\tSüleyman Demirel Kültür Merkezi Binası (Ayazağa)\n\nSMB\t\t\tSpor Merkezi Binası (Ayazağa)\n\nSTD\t\t\tİTÜ Olimpik Stadyumu  (Ayazağa)\n\nSYM\t\t\tSağlıklı Yaşam Merkezi (Ayazağa)\n\nUUB\t\t\tUçak ve Uzay Bilimleri Binası (Ayazağa)\n\nUZEM\t\t\tUzaktan Eğitim Merkezi Binası (Ayazağa)\n\nTMB\t\t\tKonservatuvar Binası (Maçka)\n\nYDB\t\t\tYapı Deprem Binası (Ayazağa)\n\nMOBGAM\t\tDr. Orhan Öcalgiray Moleküler Biyoloji-Biyoteknoloji & Genetik Araştırmalar Merkezi\n\nENB\t\t\tEnerji Binası (Ayazağa)\n\nHLB\t\t\tHidrolik Laboratuvarı Binası (Ayazağa)");
}

// Wep-App Standalone URL Fixer
$(document).ready(function () {
    if (("standalone" in window.navigator) && window.navigator.standalone) {
        // For iOS Apps
        $('a').on('click', function (e) {
            e.preventDefault();
            var new_location = $(this).attr('href');
            if (new_location != undefined && new_location.substr(0, 1) != '#' && $(this).attr('data-method') == undefined) {
                window.location = new_location;
            }
        });
    }
});
