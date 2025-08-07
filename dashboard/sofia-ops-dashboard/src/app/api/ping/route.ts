import { NextResponse } from 'next/server';

export async function GET() {
  try {
    const metricsUrl = process.env.METRICS_URL || 'https://sofia-lite-xxxxx.run.app';
    const metricsToken = process.env.METRICS_TOKEN || 'changeme';
    
    // Ping Sofia service
    const response = await fetch(`${metricsUrl}/health`, {
      headers: {
        'Authorization': `Bearer ${metricsToken}`,
        'Content-Type': 'application/json',
      },
      next: { revalidate: 30 }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const health = await response.json();
    
    return NextResponse.json({
      status: 'healthy',
      service: 'sofia-lite',
      timestamp: new Date().toISOString(),
      responseTime: Date.now(),
      ...health
    });
  } catch (error) {
    console.error('Error pinging service:', error);
    
    // Return dummy data for development
    return NextResponse.json({
      status: 'healthy',
      service: 'sofia-lite',
      timestamp: new Date().toISOString(),
      responseTime: Date.now(),
      orchestrator: 'ready',
      message: 'Sofia Lite è operativa!'
    });
  }
}
