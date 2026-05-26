import Link from 'next/link';
import Image from 'next/image';

export default function HomePage() {
  return (
    <main className="flex flex-1 flex-col items-center justify-center px-6 py-20">
      <h1 className="mb-16 text-4xl font-bold tracking-tight sm:text-5xl">
        SolidX Docs
      </h1>
      <div className="grid max-w-5xl grid-cols-1 gap-10 md:grid-cols-2">
        <Link
          href="/docs/admin-docs"
          className="hover:bg-fd-accent border-fd-border rounded-xl border p-8 transition-colors"
        >
          <h2 className="mb-4 text-2xl font-semibold">Admin</h2>
          <p className="text-fd-muted-foreground mb-6 leading-relaxed">
            A complete guide for administrators and business users to install,
            configure, and manage applications in SolidX. Learn how to set up
            modules, setup core business entities or models, manage users, and
            tailor the platform to fit your organizational needs—without writing
            code.
          </p>
          <span className="text-fd-primary font-medium">Get Started →</span>
          <div className="mt-6">
            <Image
              src="/img/homeImage-11.png"
              alt="Admin illustration"
              width={500}
              height={300}
              className="rounded-lg"
            />
          </div>
        </Link>

        <Link
          href="/docs/developer-docs"
          className="hover:bg-fd-accent border-fd-border rounded-xl border p-8 transition-colors"
        >
          <h2 className="mb-4 text-2xl font-semibold">Dev Docs</h2>
          <p className="text-fd-muted-foreground mb-6 leading-relaxed">
            Dive into SolidX&apos;s low-code engine and learn how to extend,
            customize, and integrate enterprise applications using APIs, code
            hooks, and reusable components. Ideal for developers looking to build
            advanced logic and automation on top of the platform.
          </p>
          <span className="text-fd-primary font-medium">Explore Docs →</span>
          <div className="mt-6">
            <Image
              src="/img/homeImage-22.png"
              alt="Dev Docs illustration"
              width={500}
              height={300}
              className="rounded-lg"
            />
          </div>
        </Link>
      </div>
    </main>
  );
}
