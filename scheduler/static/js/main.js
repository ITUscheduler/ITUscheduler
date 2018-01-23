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
    alert("AYB\t\tAfet Yönetimi Binası (Ayazağa)\n" +
        "--------------------------------------------------\n" +
        "BEB\t\tBilişim Enstitüsü Binası (Ayazağa)\n" +
        "--------------------------------------------------\n" +
        "DIB\t\tYabancı Diller Yüksekokulu Binası (Maçka)\n" +
        "--------------------------------------------------\n" +
        "DMB\t\tDenizcilik Meslek Yüksekokulu Binası (Ayazağa)\n" +
        "--------------------------------------------------\n" +
        "DZB\t\tDenizcilik Binası (Tuzla)\n" +
        "--------------------------------------------------\n" +
        "EEB\t\tElektrik-Elektronik Binası (Ayazağa)\n" +
        "--------------------------------------------------\n" +
        "FEB\t\tFen-Edebiyat Binası (Ayazağa)\n" +
        "--------------------------------------------------\n" +
        "GDB\t\tGemi İnşaatı ve Deniz Bilimleri Binası (Ayazağa)\n" +
        "--------------------------------------------------\n" +
        "HVZ\t\tOlimpik Havuz (Ayazağa)\n" +
        "--------------------------------------------------\n" +
        "INB\t\tİnşaat Binası (Ayazağa)\n" +
        "--------------------------------------------------\n" +
        "ISB\t\tİşletme Binası (Maçka)\n" +
        "--------------------------------------------------\n" +
        "KSB\t\tKültür ve Sanat Birliği (Ayazağa)\n" +
        "--------------------------------------------------\n" +
        "KMB\t\tKimya-Metalürji Binası (Ayazağa)\n" +
        "--------------------------------------------------\n" +
        "KORT\t\tTenis Kortları (Ayazağa)\n" +
        "--------------------------------------------------\n" +
        "MED\t\tMerkezi Derslik Binası (Ayazağa)\n" +
        "--------------------------------------------------\n" +
        "MEDB\t\tGölet Derslik Binası(Ayazağa)\n" +
        "--------------------------------------------------\n" +
        "MDB\t\tMaden Binası (Ayazağa)\n" +
        "--------------------------------------------------\n" +
        "MIAB\t\tMüzik İleri Araştırmalar Merkezi (Maçka)\n" +
        "--------------------------------------------------\n" +
        "MKB\t\tMakina Binası (Gümüşsuyu)\n" +
        "--------------------------------------------------\n" +
        "MMB\t\tMimarlık Binası (Taşkışla)\n" +
        "--------------------------------------------------\n" +
        "MOB\t\tMotorlar Binası (Ayazağa)\n" +
        "--------------------------------------------------\n" +
        "PYB\t\tProje Yönetim Merkezi (Ayazağa)\n" +
        "--------------------------------------------------\n" +
        "RSLN-M\t\tRuhi Sarıalp Seminer Salonu-Beden Eğitimi Bölümü(Ayazağa)\n" +
        "--------------------------------------------------\n" +
        "SLN-M\t\tSpor Salonu-Beden Eğitimi Bölümü(Ayazağa)\n" +
        "--------------------------------------------------\n" +
        "SLN-G\t\tSpor Salonu (Gümüşsuyu)\n" +
        "--------------------------------------------------\n" +
        "SDKM\t\tSüleyman Demirel Kültür Merkezi Binası (Ayazağa)\n" +
        "--------------------------------------------------\n" +
        "SMB\t\tSpor Merkezi Binası (Ayazağa)\n" +
        "--------------------------------------------------\n" +
        "STD\t\tİTÜ Olimpik Stadyumu  (Ayazağa)\n" +
        "--------------------------------------------------\n" +
        "SYM\t\tSağlıklı Yaşam Merkezi (Ayazağa)\n" +
        "--------------------------------------------------\n" +
        "UUB\t\tUçak ve Uzay Bilimleri Binası (Ayazağa)\n" +
        "--------------------------------------------------\n" +
        "UZEM\t\tUzaktan Eğitim Merkezi Binası (Ayazağa)\n" +
        "--------------------------------------------------\n" +
        "TMB\t\tKonservatuvar Binası (Maçka)\n" +
        "--------------------------------------------------\n" +
        "YDB\t\tYapı Deprem Binası (Ayazağa)");
}

// Wep-App Standalone URL Fixer
$(document).ready(function() {
    if (("standalone" in window.navigator) && window.navigator.standalone) {
        // For iOS Apps
        $('a').on('click', function(e) {
            e.preventDefault();
            var new_location = $(this).attr('href');
            if (new_location != undefined && new_location.substr(0, 1) != '#' && $(this).attr('data-method') == undefined) {
                window.location = new_location;
            }
        });
    }
});
