import Image from "next/image";

export default function Home() {
  return (
    <div className="min-h-screen p-8 sm:p-20 font-[family-name:var(--font-geist-mono)]">
      <main className="flex flex-col gap-12 items-center sm:items-start max-w-4xl mx-auto">

        {/* Header Section */}
        <div className="w-full border-b-2 border-white pb-6">
          <div className="flex justify-between items-center mb-4">
            <h1 className="text-4xl sm:text-6xl font-bold tracking-tighter uppercase">
              Ctrl<span className="text-green-500">+</span>Alt<span className="text-green-500">+</span>Deploy
            </h1>
            <div className="hidden sm:block text-xs border border-white px-2 py-1">
              v1.0.0-ALPHA
            </div>
          </div>
          <p className="text-xl sm:text-2xl text-gray-400 font-light">
            &gt; Cloud infrastructure deployment, <span className="text-white font-bold bg-gray-800 px-1">simplified</span>.
          </p>
        </div>

        {/* Terminal Demo Section */}
        <div className="w-full bg-black border-2 border-white p-4 shadow-[8px_8px_0px_0px_rgba(255,255,255,0.2)]">
          <div className="flex gap-2 mb-4 border-b border-gray-800 pb-2">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
            <span className="ml-2 text-xs text-gray-500">user@ctrl-alt-deploy:~/project</span>
          </div>
          <div className="font-mono text-sm sm:text-base space-y-2">
            <div>
              <span className="text-green-500">$</span> ctrl-alt-deploy init
            </div>
            <div className="text-gray-400">
              Initializing infrastructure project...
            </div>
            <div className="text-gray-400">
              &gt; Detected spec.json
            </div>
            <div className="text-gray-400">
              &gt; Analyzing dependencies...
            </div>
            <div>
              <span className="text-green-500">$</span> ctrl-alt-deploy generate --target=aws
            </div>
            <div className="text-gray-300">
              [+] Generated main.tf <span className="text-green-500">✓</span>
            </div>
            <div className="text-gray-300">
              [+] Generated ec2_instance.tf <span className="text-green-500">✓</span>
            </div>
            <div className="text-gray-300">
              [+] Generated vpc.tf <span className="text-green-500">✓</span>
            </div>
            <div>
              <span className="text-green-500">$</span> <span className="inline-block w-2 h-4 bg-green-500 cursor-blink"></span>
            </div>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 w-full">
          <div className="border border-gray-700 p-6 hover:border-white transition-colors cursor-crosshair group">
            <h3 className="text-lg font-bold mb-2 group-hover:text-green-500 transition-colors">&gt; Terraform Gen</h3>
            <p className="text-sm text-gray-400">
              Auto-convert JSON specifications into production-ready Terraform configuration files.
            </p>
          </div>

          <div className="border border-gray-700 p-6 hover:border-white transition-colors cursor-crosshair group">
            <h3 className="text-lg font-bold mb-2 group-hover:text-green-500 transition-colors">&gt; Multi-Cloud</h3>
            <p className="text-sm text-gray-400">
              Engineered for AWS, designed to scale for Azure and GCP in future updates.
            </p>
          </div>

          <div className="border border-gray-700 p-6 hover:border-white transition-colors cursor-crosshair group">
            <h3 className="text-lg font-bold mb-2 group-hover:text-green-500 transition-colors">&gt; Docker Native</h3>
            <p className="text-sm text-gray-400">
              Seamlessly deploy containerized applications with auto-generated user data scripts.
            </p>
          </div>
        </div>

        {/* CTA */}
        <div className="flex gap-4 items-center flex-col sm:flex-row mt-4">
          <a
            className="border-2 border-white bg-white text-black text-sm sm:text-base h-10 sm:h-12 px-8 flex items-center justify-center font-bold hover:bg-transparent hover:text-white transition-all uppercase tracking-wider shadow-[4px_4px_0px_0px_rgba(255,255,255,1)] hover:shadow-[2px_2px_0px_0px_rgba(255,255,255,1)] hover:translate-x-[2px] hover:translate-y-[2px]"
            href="#"
          >
            Start Deploying
          </a>
          <a
            className="text-sm sm:text-base h-10 sm:h-12 px-8 flex items-center justify-center hover:text-green-500 transition-colors border border-transparent hover:border-gray-800"
            href="#"
          >
            Read Documentation &rarr;
          </a>
        </div>
      </main>

      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center mt-24 text-gray-600 text-xs uppercase tracking-widest">
        <p>System Status: <span className="text-green-500">ONLINE</span></p>
        <p>Region: US-EAST-1</p>
      </footer>
    </div>
  );
}
