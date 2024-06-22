/**
 * v0 by Vercel.
 * @see https://v0.dev/t/jGBXhQHojVi
 * Documentation: https://v0.dev/docs#integrating-generated-code-into-your-nextjs-app
 */
import { Button } from "./ui/button"
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from "./ui/accordion"
import { Label } from "./ui/label"
import { Checkbox } from "./ui/checkbox"

export default function Component() {
  return (
    <div className="flex flex-col min-h-[100dvh]">
      <header className="flex h-16 items-center justify-between px-4 md:px-6 border-b">
        <a href="#" className="flex items-center gap-2" >
          <MountainIcon className="h-6 w-6" />
          <span className="text-lg font-semibold">Acme Inc</span>
        </a>
        <nav className="hidden md:flex gap-4">
          <a href="#" className="text-sm font-medium hover:underline" >
            Home
          </a>
          <a href="#" className="text-sm font-medium hover:underline" >
            Products
          </a>
          <a href="#" className="text-sm font-medium hover:underline" >
            About
          </a>
          <a href="#" className="text-sm font-medium hover:underline" >
            Contact
          </a>
        </nav>
        <div className="flex items-center gap-2 md:hidden">
          <Button variant="ghost" size="icon">
            <MenuIcon className="h-6 w-6" />
            <span className="sr-only">Toggle menu</span>
          </Button>
        </div>
      </header>
      <main className="flex-1">
        <section className="py-8 md:py-12 lg:py-16">
          <div className="container px-4 md:px-6">
            <div className="mb-6 md:mb-8 lg:mb-10">
              <Accordion type="single" collapsible>
                <AccordionItem value="filters">
                  <AccordionTrigger className="flex items-center justify-between">
                    <span className="text-lg font-medium">Filters</span>
                    <ChevronDownIcon className="h-5 w-5 transition-transform group-[data-state=open]:rotate-180" />
                  </AccordionTrigger>
                  <AccordionContent>
                    <div className="grid gap-4">
                      <div>
                        <h3 className="mb-2 text-sm font-medium">Category</h3>
                        <div className="grid gap-2">
                          <Label className="flex items-center gap-2 font-normal">
                            <Checkbox id="category-1" /> Category 1
                          </Label>
                          <Label className="flex items-center gap-2 font-normal">
                            <Checkbox id="category-2" /> Category 2
                          </Label>
                          <Label className="flex items-center gap-2 font-normal">
                            <Checkbox id="category-3" /> Category 3
                          </Label>
                          <Label className="flex items-center gap-2 font-normal">
                            <Checkbox id="category-4" /> Category 4
                          </Label>
                        </div>
                      </div>
                      <div>
                        <h3 className="mb-2 text-sm font-medium">Price</h3>
                        <div className="grid gap-2">
                          <Label className="flex items-center gap-2 font-normal">
                            <Checkbox id="price-1" /> $0 - $50
                          </Label>
                          <Label className="flex items-center gap-2 font-normal">
                            <Checkbox id="price-2" /> $50 - $100
                          </Label>
                          <Label className="flex items-center gap-2 font-normal">
                            <Checkbox id="price-3" /> $100 - $200
                          </Label>
                          <Label className="flex items-center gap-2 font-normal">
                            <Checkbox id="price-4" /> $200+
                          </Label>
                        </div>
                      </div>
                    </div>
                  </AccordionContent>
                </AccordionItem>
              </Accordion>
            </div>
            <div className="overflow-auto">
              <table className="w-full border-collapse">
                <thead>
                  <tr className="bg-muted">
                    <th className="px-4 py-3 text-left font-medium">Product</th>
                    <th className="px-4 py-3 text-left font-medium">Description</th>
                    <th className="px-4 py-3 text-right font-medium">Price</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-b">
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-4">
                        <img
                          src="/placeholder.svg"
                          alt="Product 1"
                          width={80}
                          height={60}
                          className="object-cover rounded-lg"
                        />
                        <h3 className="text-lg font-semibold">Stylish Sunglasses</h3>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-muted-foreground">UV protection</td>
                    <td className="px-4 py-3 text-right font-semibold">$29.99</td>
                  </tr>
                  <tr className="border-b">
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-4">
                        <img
                          src="/placeholder.svg"
                          alt="Product 2"
                          width={80}
                          height={60}
                          className="object-cover rounded-lg"
                        />
                        <h3 className="text-lg font-semibold">Leather Crossbody Bag</h3>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-muted-foreground">Stylish and practical</td>
                    <td className="px-4 py-3 text-right font-semibold">$49.99</td>
                  </tr>
                  <tr className="border-b">
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-4">
                        <img
                          src="/placeholder.svg"
                          alt="Product 3"
                          width={80}
                          height={60}
                          className="object-cover rounded-lg"
                        />
                        <h3 className="text-lg font-semibold">Wireless Headphones</h3>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-muted-foreground">High-quality sound</td>
                    <td className="px-4 py-3 text-right font-semibold">$79.99</td>
                  </tr>
                  <tr className="border-b">
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-4">
                        <img
                          src="/placeholder.svg"
                          alt="Product 4"
                          width={80}
                          height={60}
                          className="object-cover rounded-lg"
                        />
                        <h3 className="text-lg font-semibold">Classic Wristwatch</h3>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-muted-foreground">Timeless design</td>
                    <td className="px-4 py-3 text-right font-semibold">$59.99</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>
      </main>
      <footer className="flex flex-col gap-2 sm:flex-row py-6 w-full shrink-0 items-center px-4 md:px-6 border-t">
        <p className="text-xs text-muted-foreground">&copy; 2024 Acme Inc. All rights reserved.</p>
        <nav className="sm:ml-auto flex gap-4 sm:gap-6">
          <a href="#" className="text-xs hover:underline underline-offset-4" >
            Terms of Service
          </a>
          <a href="#" className="text-xs hover:underline underline-offset-4" >
            Privacy
          </a>
        </nav>
      </footer>
    </div>
  )
}

function ChevronDownIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="m6 9 6 6 6-6" />
    </svg>
  )
}


function MenuIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <line x1="4" x2="20" y1="12" y2="12" />
      <line x1="4" x2="20" y1="6" y2="6" />
      <line x1="4" x2="20" y1="18" y2="18" />
    </svg>
  )
}


function MountainIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="m8 3 4 8 5-5 5 15H2L8 3z" />
    </svg>
  )
}