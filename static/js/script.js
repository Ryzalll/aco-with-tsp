const btn_jumlah_kota = document.getElementById('btn_jmlh_kota');
const form_kota = document.getElementById('form_kota');
const jumlah_kota_input = document.getElementById('jumlah_kota');

btn_jumlah_kota.addEventListener('click', () => {
    let jumlah_kota = parseInt(jumlah_kota_input.value);

    // Clear existing inputs before adding new ones
    form_kota.innerHTML = '';

    if (isNaN(jumlah_kota) || jumlah_kota <= 0) {
        alert("Mohon masukkan jumlah kota yang valid (angka positif).");
        return;
    }

    for (let i = 0; i < jumlah_kota; i++) {
        // Create a div to group related inputs for better styling
        const inputGroup = document.createElement('div');
        inputGroup.classList.add('input-group');

        const inputCityName = document.createElement('input');
        inputCityName.type = 'text';
        inputCityName.name = 'kota-' + i;
        inputCityName.placeholder = 'Masukkan Nama Kota ke -' + (i + 1); // Start counting from 1 for user clarity
        inputCityName.required = true; // Make city name required

        const koor_x = document.createElement('input');
        koor_x.type = 'number';
        koor_x.name = 'x-kota-' + i;
        koor_x.placeholder = "Masukkan koordinat X kota ke -" + (i + 1);
        koor_x.required = true; // Make coordinate X required

        const koor_y = document.createElement('input');
        koor_y.type = 'number';
        koor_y.name = 'y-kota-' + i;
        koor_y.placeholder = "Masukkan koordinat Y kota ke -" + (i + 1);
        koor_y.required = true; // Make coordinate Y required

        inputGroup.appendChild(inputCityName);
        inputGroup.appendChild(koor_x);
        inputGroup.appendChild(koor_y);
        form_kota.appendChild(inputGroup);
    }

    const jumlah_semut = document.createElement("input");
    jumlah_semut.type = "number";
    jumlah_semut.name = "jumlah_semut"
    jumlah_semut.placeholder = "Masukkan jumlah semut"
    form_kota.appendChild(jumlah_semut);
    const jumlah_iterasi = document.createElement("input");
    jumlah_iterasi.type = "number"
    jumlah_iterasi.name = "jumlah_iterasi"
    jumlah_iterasi.placeholder = "Masukkan jumlah iterasi"
    form_kota.appendChild(jumlah_iterasi);
    const submitButton = document.createElement("button");
    submitButton.type = 'submit';
    submitButton.innerHTML = "Submit";
    form_kota.appendChild(submitButton);
});