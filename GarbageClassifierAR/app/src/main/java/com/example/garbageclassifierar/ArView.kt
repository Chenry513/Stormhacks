package com.example.garbageclassifierar

import android.content.Context
import android.opengl.GLSurfaceView
import android.view.View
import android.widget.TextView
import com.google.ar.core.ArCoreApk
import com.google.ar.core.Session
import com.google.ar.core.exceptions.CameraNotAvailableException

class ArView(context: Context, resultsText: TextView) : GLSurfaceView(context) {

    private var session: Session? = null

    init {
        // Set up the OpenGL ES context
        setEGLContextClientVersion(2)
        // Set the renderer
        session = Session(context)
        setRenderer(ArRenderer(context, session!!, resultsText))
        // Set the render mode to render continuously
        renderMode = RENDERMODE_CONTINUOUSLY
    }

    fun onResume() {
        // Check if ARCore is installed
        if (session == null) {
            try {
                // Create a new ARCore session
                session = Session(context)
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }

        try {
            // Resume the ARCore session
            session?.resume()
        } catch (e: CameraNotAvailableException) {
            e.printStackTrace()
        }

        // Resume the GLSurfaceView
        super.onResume()
    }

    fun onPause() {
        // Pause the GLSurfaceView
        super.onPause()
        // Pause the ARCore session
        session?.pause()
    }

    fun getSession(): Session? {
        return session
    }
}
