-- CreateTable
CREATE TABLE "Song" (
    "id" UUID NOT NULL,
    "song" TEXT NOT NULL,
    "thumbnail" TEXT NOT NULL,
    "artist" TEXT NOT NULL,
    "song_name" TEXT NOT NULL,
    "hex_color" TEXT NOT NULL,
    "userId" UUID NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Song_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "Song" ADD CONSTRAINT "Song_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
