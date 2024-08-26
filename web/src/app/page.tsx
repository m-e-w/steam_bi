import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <Card className="w-[350px]">
        <CardHeader>
          <CardTitle>Enter your Steam ID</CardTitle>
          <CardDescription>
            Lorem
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form>
            <div className="grid w-full items-center gap-4">
              <div className="flex flex-col space-y-1.5">
                <Label htmlFor="steamid">Steam ID</Label>
                <Input id="steamid" placeholder="Your Steam ID" />
              </div>
            </div>
          </form>
        </CardContent>
        <CardFooter className="flex">
          <Button>Submit</Button>
        </CardFooter>
      </Card>
    </main>
  );
}
