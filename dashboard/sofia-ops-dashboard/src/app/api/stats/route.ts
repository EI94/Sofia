import { NextResponse } from 'next/server';
import { readFileSync } from 'fs';
import { join } from 'path';

export async function GET() {
  try {
    const metricsUrl = process.env.METRICS_URL;
    
    // If no METRICS_URL is configured, use mock data
    if (!metricsUrl) {
      const mockDataPath = join(process.cwd(), 'mock', 'stats.json');
      const mockData = JSON.parse(readFileSync(mockDataPath, 'utf-8'));
      
      return NextResponse.json({
        newLeads: mockData.leadsRate * 10, // Convert rate to total
        activeConversations: mockData.bookingsRate * 15, // Convert rate to total
        responseTime: mockData.p95[1]?.v || 1.44, // Use latest P95 value
        errorRate: (100 - mockData.successRatio[0]?.value) / 100 || 0.02, // Convert success to error rate
        uptime: 99.8,
        lastUpdate: new Date().toISOString(),
        mockData: true // Flag to indicate this is mock data
      });
    }
    
    const metricsToken = process.env.METRICS_TOKEN || 'changeme';
    
    // Fetch metrics from Sofia service
    const response = await fetch(`${metricsUrl}/metrics`, {
      headers: {
        'Authorization': `Bearer ${metricsToken}`,
        'Content-Type': 'application/json',
      },
      next: { revalidate: 30 }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const metrics = await response.text();
    
    // Parse Prometheus metrics and convert to JSON
    const stats = parsePrometheusMetrics(metrics);
    
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

function parsePrometheusMetrics(metrics: string) {
  const lines = metrics.split('\n');
  const stats: Record<string, number> = {};
  
  for (const line of lines) {
    if (line.startsWith('sofia_new_leads_total')) {
      const match = line.match(/(\d+)/);
      if (match) stats.newLeads = parseInt(match[1]);
    }
    if (line.startsWith('sofia_conversations_total')) {
      const match = line.match(/(\d+)/);
      if (match) stats.activeConversations = parseInt(match[1]);
    }
    if (line.startsWith('sofia_response_time_seconds')) {
      const match = line.match(/(\d+\.\d+)/);
      if (match) stats.responseTime = parseFloat(match[1]);
    }
    if (line.startsWith('sofia_error_rate')) {
      const match = line.match(/(\d+\.\d+)/);
      if (match) stats.errorRate = parseFloat(match[1]);
    }
  }
  
  return {
    ...stats,
    uptime: 99.8,
    lastUpdate: new Date().toISOString()
  };
}
