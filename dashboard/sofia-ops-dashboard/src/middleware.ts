import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  // Skip auth for API routes and static files
  if (request.nextUrl.pathname.startsWith('/api/') || 
      request.nextUrl.pathname.startsWith('/_next/') ||
      request.nextUrl.pathname.includes('.')) {
    return NextResponse.next();
  }

  const authHeader = request.headers.get('authorization');
  const expectedUser = process.env.BASIC_AUTH_USER || 'opsviewer';
  const expectedPass = process.env.BASIC_AUTH_PASS || 'strongpassword';
  
  // Create expected auth string
  const expectedAuth = `Basic ${Buffer.from(`${expectedUser}:${expectedPass}`).toString('base64')}`;
  
  if (authHeader !== expectedAuth) {
    return new NextResponse('Authentication required', {
      status: 401,
      headers: {
        'WWW-Authenticate': 'Basic realm="Sofia Ops Dashboard"',
      },
    });
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};
