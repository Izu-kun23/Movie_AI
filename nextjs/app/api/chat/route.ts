import { NextRequest, NextResponse } from 'next/server';

// Proxy to Python backend
const BACKEND_URL = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_BACKEND_URL || 'http://127.0.0.1:8000';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // Check if backend URL is configured
    if (!BACKEND_URL || BACKEND_URL === 'http://127.0.0.1:8000') {
      console.error('BACKEND_URL not configured. Please set it in Vercel environment variables.');
      return NextResponse.json(
        { 
          error: 'Backend not configured. Please set BACKEND_URL environment variable.',
          type: 'error',
          message: 'The backend API URL is not configured. Please set the BACKEND_URL environment variable in Vercel settings.'
        },
        { status: 500 }
      );
    }
    
    const response = await fetch(`${BACKEND_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Backend request failed' }));
      return NextResponse.json(
        { 
          error: error.detail || 'Backend request failed',
          type: 'error',
          message: error.detail || `Backend returned ${response.status} status`
        },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error: any) {
    console.error('API route error:', error);
    return NextResponse.json(
      { 
        error: error.message || 'Internal server error',
        type: 'error',
        message: error.message || 'Failed to connect to backend. Please check your BACKEND_URL configuration.'
      },
      { status: 500 }
    );
  }
}

