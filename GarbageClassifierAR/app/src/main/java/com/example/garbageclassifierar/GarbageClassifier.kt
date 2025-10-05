package com.example.garbageclassifierar

import android.content.Context
import android.graphics.Bitmap
import org.tensorflow.lite.Interpreter
import java.io.FileInputStream
import java.nio.ByteBuffer
import java.nio.ByteOrder
import java.nio.channels.FileChannel

class GarbageClassifier(context: Context) {

    private val interpreter: Interpreter
    private val labels: List<String>

    init {
        // Load the model
        val model = loadModelFile(context, "model.tflite")
        interpreter = Interpreter(model)

        // Load the labels
        labels = loadLabels(context, "labels.txt")
    }

    private fun loadModelFile(context: Context, modelName: String): ByteBuffer {
        val assetFileDescriptor = context.assets.openFd(modelName)
        val fileInputStream = FileInputStream(assetFileDescriptor.fileDescriptor)
        val fileChannel = fileInputStream.channel
        val startOffset = assetFileDescriptor.startOffset
        val declaredLength = assetFileDescriptor.declaredLength
        return fileChannel.map(FileChannel.MapMode.READ_ONLY, startOffset, declaredLength)
    }

    private fun loadLabels(context: Context, labelFile: String): List<String> {
        return context.assets.open(labelFile).bufferedReader().useLines { it.toList() }
    }

    fun classify(bitmap: Bitmap): String {
        // Preprocess the image
        val input = preprocessImage(bitmap)

        // Run the inference
        val output = Array(1) { FloatArray(6) }
        interpreter.run(input, output)

        // Postprocess the results
        return postprocessResults(output)
    }

    private fun preprocessImage(bitmap: Bitmap): ByteBuffer {
        val resizedBitmap = Bitmap.createScaledBitmap(bitmap, 320, 320, true)
        val byteBuffer = ByteBuffer.allocateDirect(4 * 320 * 320 * 3)
        byteBuffer.order(ByteOrder.nativeOrder())
        val intValues = IntArray(320 * 320)
        resizedBitmap.getPixels(intValues, 0, resizedBitmap.width, 0, 0, resizedBitmap.width, resizedBitmap.height)
        var pixel = 0
        for (i in 0 until 320) {
            for (j in 0 until 320) {
                val `val` = intValues[pixel++]
                byteBuffer.putFloat(((`val` shr 16) and 0xFF) / 255.0f)
                byteBuffer.putFloat(((`val` shr 8) and 0xFF) / 255.0f)
                byteBuffer.putFloat((`val` and 0xFF) / 255.0f)
            }
        }
        return byteBuffer
    }

    private fun postprocessResults(output: Array<FloatArray>): String {
        val scores = output[0]
        var maxScore = -1f
        var maxIndex = -1
        for (i in scores.indices) {
            if (scores[i] > maxScore) {
                maxScore = scores[i]
                maxIndex = i
            }
        }
        return labels[maxIndex]
    }
}
