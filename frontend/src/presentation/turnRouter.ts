import express from 'express'
import { Point } from '../domain/model/turn/point'
import { toDisc } from '../domain/model/turn/disc'
import { GameMySQLRepository } from '../infrastructure/repository/game/gameMySQLRepository'
import { TurnMySQLRepository } from '../infrastructure/repository/turn/turnMySQLRepository'
import { GameResultMySQLRepository } from '../infrastructure/repository/gameResult/gameResultMySQLRepository'
import { RegisterTurnUseCase } from '../application/useCase/registerTurnUseCase'
import { FindLatestGameTurnByTurnCountUseCase } from '../application/useCase/findLatestGameTurnByTurnCountUseCase'

export const turnRouter = express.Router()

const findLatestGameTurnByTurnCountUseCase =
  new FindLatestGameTurnByTurnCountUseCase(
    new GameMySQLRepository(),
    new TurnMySQLRepository(),
    new GameResultMySQLRepository()
  )

const registerTurnUseCase = new RegisterTurnUseCase(
  new GameMySQLRepository(),
  new TurnMySQLRepository(),
  new GameResultMySQLRepository()
)

interface TurnGetResponseBody {
  turnCount: number
  board: number[][]
  nextDisc: number | null
  winnerDisc: number | null
}

turnRouter.get(
  '/api/games/latest/turns/:turnCount',
  async (req, res: express.Response<TurnGetResponseBody>) => {
    const turnCount = parseInt(req.params.turnCount)

    const output = await findLatestGameTurnByTurnCountUseCase.run(turnCount)

    const responseBody = {
      turnCount: output.turnCount,
      board: output.board,
      nextDisc: output.nextDisc ?? null,
      winnerDisc: output.winnerDisc ?? null
    }

    res.json(responseBody)
  }
)

interface TurnPostRequestBody {
  turnCount: number
  move: {
    disc: number
    x: number
    y: number
  }
}

turnRouter.post(
  '/api/games/latest/turns',
  async (req: express.Request<{}, {}, TurnPostRequestBody>, res) => {
    const turnCount = req.body.turnCount
    const disc = toDisc(req.body.move.disc)
    const point = new Point(req.body.move.x, req.body.move.y)

    await registerTurnUseCase.run(turnCount, disc, point)

    res.status(201).end()
  }
)
