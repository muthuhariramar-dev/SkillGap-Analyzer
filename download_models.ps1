$baseUrl = "https://github.com/justadudewhohacks/face-api.js/raw/master/weights"
$models = @(
    "tiny_face_detector_model-weights_manifest.json",
    "tiny_face_detector_model-shard1",
    "face_landmark_68_model-weights_manifest.json",
    "face_landmark_68_model-shard1",
    "face_recognition_model-weights_manifest.json",
    "face_recognition_model-shard1",
    "face_recognition_model-shard2",
    "face_expression_model-weights_manifest.json",
    "face_expression_model-shard1"
)

$outputDir = "c:\Users\User\Downloads\Skills-Gap-Analysis-with-Generative-AI-main\Skills-Gap-Analysis-with-Generative-AI-main\frontend\public\models"

foreach ($model in $models) {
    $url = "$baseUrl/$model"
    $output = "$outputDir\$model"
    Write-Host "Downloading $model..."
    Invoke-WebRequest -Uri $url -OutFile $output
}
