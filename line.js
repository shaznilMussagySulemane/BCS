const process = require('process');

console.log("Iniciando Download!");

function updateProgress(progress) {
    process.stdout.write(`Progresso: ${progress}%\r`);
    // console.log(`Progress: ${progress}%\r`);
    
}

// Simulando um download (substitua por sua lógica de download)
for (let i = 0; i <= 10000; i++) {
    updateProgress(i / 100);
    // Simulando um atraso
    // new Promise(resolve => setTimeout(resolve, 100));
}

console.log('\nDownload completo!');