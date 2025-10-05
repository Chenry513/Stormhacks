package com.example.garbageclassifierar

import android.content.Context
import android.graphics.Bitmap
import android.opengl.GLES20
import android.opengl.GLSurfaceView
import android.util.Log
import android.widget.TextView
import com.google.ar.core.Frame
import com.google.ar.core.Session
import javax.microedition.khronos.egl.EGLConfig
import javax.microedition.khronos.opengles.GL10

class ArRenderer(private val context: Context, private val session: Session, private val resultsText: TextView) : GLSurfaceView.Renderer {

    private lateinit var garbageClassifier: GarbageClassifier

    override fun onSurfaceCreated(gl: GL10?, config: EGLConfig?) {
        // Set the background color to black
        GLES20.glClearColor(0.0f, 0.0f, 0.0f, 1.0f)

        // Initialize the garbage classifier
        garbageClassifier = GarbageClassifier(context)
    }

    override fun onSurfaceChanged(gl: GL10?, width: Int, height: Int) {
        // Set the viewport
        GLES20.glViewport(0, 0, width, height)
    }

    override fun onDrawFrame(gl: GL10?) {
        // Clear the screen
        GLES20.glClear(GLES20.GL_COLOR_BUFFER_BIT or GLES20.GL_DEPTH_BUFFER_BIT)

        // Get the current frame
        val frame = session.update()

        // Get the camera image
        val image = frame.acquireCameraImage()

        // Convert the image to a bitmap
        val bitmap = Bitmap.createBitmap(image.width, image.height, Bitmap.Config.ARGB_8888)
        image.use { it.copyPixelsToBuffer(bitmap.byteBuffer) }

        // Classify the image
        val result = garbageClassifier.classify(bitmap)

        // Log the results
        Log.d("ArRenderer", "Result: $result")

        // Update the TextView
        resultsText.post {
            resultsText.text = result
        }
    }
}
