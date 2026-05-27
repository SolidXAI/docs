import Link from 'next/link';
import Image from 'next/image';

export default function HomePage() {
  return (
    <main className="flex flex-1 flex-col items-center justify-center px-6 py-20">
      <div className="mb-16 flex flex-col items-center text-center">
        <h1 className="flex items-center gap-3 text-4xl font-bold tracking-tight sm:text-5xl">
          <img src="/img/NavbarLogo.svg" alt="SolidX" className="h-9 sm:h-11" />
          <span>Docs</span>
        </h1>
        <p className="text-fd-muted-foreground mt-4 max-w-md text-lg">
          Everything you need to build, extend, and manage applications on the
          SolidX platform.
        </p>
        <Link
          href="/docs/quick-start"
          className="mt-8 inline-flex items-center gap-2 rounded-full bg-fd-primary px-7 py-3.5 text-base font-semibold text-fd-primary-foreground shadow-md transition-all hover:opacity-90 hover:shadow-lg active:scale-[0.97]"
        >
          Quick-Start
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M5 12h14" />
            <path d="m12 5 7 7-7 7" />
          </svg>
        </Link>
      </div>
      <div className="grid max-w-5xl grid-cols-1 gap-8 md:grid-cols-2">
        <Link
          href="/docs/admin-docs"
          className="group border-fd-border hover:bg-fd-accent/50 rounded-xl border p-8 transition-all hover:-translate-y-0.5 hover:shadow-md"
        >
          <div className="flex items-center gap-2">
            <span className="bg-fd-primary/10 text-fd-primary inline-flex size-8 items-center justify-center rounded-lg text-lg font-bold">
              A
            </span>
            <h2 className="text-2xl font-semibold">Admin</h2>
          </div>
          <p className="text-fd-muted-foreground mt-4 mb-6 leading-relaxed">
            A complete guide for administrators and business users to install,
            configure, and manage applications in SolidX — without writing code.
          </p>
          <span className="text-fd-primary group-hover:gap-3 inline-flex items-center gap-2 font-medium transition-all">
            Get Started
            <span className="text-lg transition-transform group-hover:translate-x-0.5">
              →
            </span>
          </span>
          <div className="mt-6 overflow-hidden rounded-lg border">
            <Image
              src="/img/homeImage-11.png"
              alt="Admin illustration"
              width={500}
              height={300}
              className="w-full transition-transform duration-300 group-hover:scale-[1.02]"
            />
          </div>
        </Link>

        <Link
          href="/docs/developer-docs"
          className="group border-fd-border hover:bg-fd-accent/50 rounded-xl border p-8 transition-all hover:-translate-y-0.5 hover:shadow-md"
        >
          <div className="flex items-center gap-2">
            <span className="bg-fd-primary/10 text-fd-primary inline-flex size-8 items-center justify-center rounded-lg text-lg font-bold">
              D
            </span>
            <h2 className="text-2xl font-semibold">Dev Docs</h2>
          </div>
          <p className="text-fd-muted-foreground mt-4 mb-6 leading-relaxed">
            Dive into SolidX&apos;s low-code engine and learn how to extend,
            customize, and integrate enterprise applications using APIs, code
            hooks, and reusable components.
          </p>
          <span className="text-fd-primary group-hover:gap-3 inline-flex items-center gap-2 font-medium transition-all">
            Explore Docs
            <span className="text-lg transition-transform group-hover:translate-x-0.5">
              →
            </span>
          </span>
          <div className="mt-6 overflow-hidden rounded-lg border">
            <Image
              src="/img/homeImage-22.png"
              alt="Dev Docs illustration"
              width={500}
              height={300}
              className="w-full transition-transform duration-300 group-hover:scale-[1.02]"
            />
          </div>
        </Link>
      </div>
    </main>
  );
}
