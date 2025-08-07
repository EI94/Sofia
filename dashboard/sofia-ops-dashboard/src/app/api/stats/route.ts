import { NextResponse } from 'next/server';
import { mapSummaryToDashboard, type SummaryMetrics } from '@/lib/mapSummary';

export const runtime = 'edge';

export async function GET() {
  try {
    const metricsUrl = process.env.METRICS_URL;
    
    // If no METRICS_URL is configured, return dummy data
    if (!metricsUrl) {
      return NextResponse.json({
        newLeads: 30,
        activeConversations: 30,
        responseTime: 1.9,
        errorRate: 0.08,
        uptime: 99.8,
        lastUpdate: new Date().toISOString(),
        mockData: true
      });
    }
    
    const metricsToken = process.env.METRICS_TOKEN || 'changeme';
    
    // Fetch summary metrics from Sofia service
    const response = await fetch(`${metricsUrl}/metrics/summary`, {
      headers: {
        'Authorization': `Bearer ${metricsToken}`,
        'Content-Type': 'application/json',
      },
      next: { revalidate: 30 }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const summary: SummaryMetrics = await response.json();
    
    // Map summary to dashboard format
    const stats = mapSummaryToDashboard(summary);
    
    return NextResponse.json(stats);
  } catch (error) {
    console.error('Error fetching stats:', error);
    
    // Return dummy data for development
    return NextResponse.json({
      newLeads: 42,
      activeConversations: 156,
      responseTime: 1.44,
      errorRate: 0.02,
      uptime: 99.8,
      lastUpdate: new Date().toISOString()
    });
  }
}
